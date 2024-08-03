#include <Python.h>
#include <rime_api.h>

#include "__init__.h"
#include "config.h"

#define DEFAULT_BUFFER_SIZE 1024

#define PY_MEMBER_Composition(name) PY_MEMBER(Composition, name)
PY_NEW_OBJECT(Composition, length, cursor_pos, sel_start, sel_end, preedit)

#define PY_MEMBER_Candidate(name) PY_MEMBER(Candidate, name)
PY_NEW_OBJECT(Candidate, text, comment)

#define PY_MEMBER_Menu(name) PY_MEMBER(Menu, name)
PY_NEW_OBJECT(Menu, page_size, page_no, is_last_page,
              highlighted_candidate_index, num_candidates, select_keys,
              candidates)

#define PY_MEMBER_Context(name) PY_MEMBER(Context, name)
PY_NEW_OBJECT(Context, composition, menu)

#define PY_MEMBER_Commit(name) PY_MEMBER(Commit, name)
PY_NEW_OBJECT(Commit, text)

#define PY_MEMBER_SchemaListItem(name) PY_MEMBER(SchemaListItem, name)
PY_NEW_OBJECT(SchemaListItem, schema_id, name)

static PyObject *init(PyObject *self, PyObject *args, PyObject *kwargs) {
  static char *keywords[] = {
      "shared_data_dir",   "user_data_dir",          "log_dir",
      "distribution_name", "distribution_code_name", "distribution_version",
      "app_name",          "min_log_level",          NULL,
  };
  RIME_STRUCT(RimeTraits, rime_traits);
  if (!PyArg_ParseTupleAndKeywords(
          args, kwargs, "sssssss|i", keywords, &rime_traits.shared_data_dir,
          &rime_traits.user_data_dir, &rime_traits.log_dir,
          &rime_traits.distribution_name, &rime_traits.distribution_code_name,
          &rime_traits.distribution_version, &rime_traits.app_name,
          &rime_traits.min_log_level))
    return NULL;
  RimeSetup(&rime_traits);
  RimeInitialize(&rime_traits);
  Py_RETURN_NONE;
}

static PyObject *createSession(PyObject *self) {
  RimeSessionId session_id = RimeCreateSession();
  if (session_id == 0) {
    PyErr_SetString(PyExc_ValueError, "failed to create session");
    return NULL;
  }
  return PyLong_FromLong(session_id);
}

static PyObject *destroySession(PyObject *self, PyObject *args) {
  RimeSessionId session_id;
  if (!PyArg_ParseTuple(args, "k|", &session_id))
    return NULL;
  if (!RimeDestroySession(session_id))
    PyErr_SetString(PyExc_ValueError, "failed to destroy session");
  Py_RETURN_NONE;
}

static PyObject *getCurrentSchema(PyObject *self, PyObject *args) {
  RimeSessionId session_id;
  if (!PyArg_ParseTuple(args, "k|", &session_id))
    return NULL;
  char schema_id[DEFAULT_BUFFER_SIZE];
  if (!RimeGetCurrentSchema(session_id, schema_id, DEFAULT_BUFFER_SIZE)) {
    PyErr_SetString(PyExc_ValueError, "failed to get current schema");
    return NULL;
  }
  return PyUnicode_FromString(schema_id);
}

static PyObject *getSchemaList(PyObject *self) {
  RimeSchemaList schema_list;
  if (!RimeGetSchemaList(&schema_list)) {
    PyErr_SetString(PyExc_ValueError, "failed to get schema list");
    return NULL;
  }
  PyObject *schema_list_item_objs = PyList_New(schema_list.size);
  for (int i = 0; i < schema_list.size; i++) {
    RimeSchemaListItem schema_list_item = schema_list.list[i];
    PyObject *schema_list_item_obj =
        PyObject_CallObject((PyObject *)&SchemaListItemType,
                            Py_BuildValue("(ss)", schema_list_item.schema_id,
                                          schema_list_item.name));
    PyList_SetItem(schema_list_item_objs, i, schema_list_item_obj);
  }
  return schema_list_item_objs;
}

static PyObject *selectSchema(PyObject *self, PyObject *args) {
  RimeSessionId session_id;
  char *schema_id;
  if (!PyArg_ParseTuple(args, "ks|", &session_id, &schema_id))
    return NULL;
  if (!RimeSelectSchema(session_id, schema_id))
    PyErr_SetString(PyExc_ValueError, "failed to select schema");
  Py_RETURN_NONE;
}

static PyObject *processKey(PyObject *self, PyObject *args) {
  RimeSessionId session_id;
  int keycode, mask = 0;
  if (!PyArg_ParseTuple(args, "ki|i", &session_id, &keycode, &mask))
    return NULL;
  return PyBool_FromLong(RimeProcessKey(session_id, keycode, mask));
}

static PyObject *getContext(PyObject *self, PyObject *args) {
  RimeSessionId session_id;
  if (!PyArg_ParseTuple(args, "k|", &session_id))
    return NULL;
  RIME_STRUCT(RimeContext, context);
  if (!RimeGetContext(session_id, &context)) {
    PyErr_SetString(PyExc_ValueError, "failed to get context");
    return NULL;
  }
  PyObject *candidate_objs = PyList_New(context.menu.num_candidates);
  for (int i = 0; i < context.menu.num_candidates; i++) {
    RimeCandidate candidate = context.menu.candidates[i];
    PyObject *candidate_obj = PyObject_CallObject(
        (PyObject *)&CandidateType,
        Py_BuildValue("(sz)", candidate.text, candidate.comment));
    PyList_SetItem(candidate_objs, i, candidate_obj);
  }
  PyObject *menu_obj = PyObject_CallObject(
      (PyObject *)&MenuType,
      Py_BuildValue("(iiiiizO)", context.menu.page_size, context.menu.page_no,
                    context.menu.is_last_page,
                    context.menu.highlighted_candidate_index,
                    context.menu.num_candidates, context.menu.select_keys,
                    candidate_objs));
  PyObject *composition_obj = PyObject_CallObject(
      (PyObject *)&CompositionType,
      Py_BuildValue("(iiiiz)", context.composition.length,
                    context.composition.cursor_pos,
                    context.composition.sel_start, context.composition.sel_end,
                    context.composition.preedit));
  PyObject *context_obj =
      PyObject_CallObject((PyObject *)&ContextType,
                          Py_BuildValue("(OO)", composition_obj, menu_obj));
  if (!RimeFreeContext(&context)) {
    PyErr_SetString(PyExc_ValueError, "failed to free context");
  }
  return context_obj;
}

static PyObject *getCommit(PyObject *self, PyObject *args) {
  RimeSessionId session_id;
  if (!PyArg_ParseTuple(args, "k|", &session_id))
    return NULL;
  RIME_STRUCT(RimeCommit, commit);
  if (!RimeGetCommit(session_id, &commit)) {
    PyErr_SetString(PyExc_ValueError, "failed to get commit");
    return NULL;
  }
  PyObject *commit_obj = PyObject_CallObject((PyObject *)&CommitType,
                                             Py_BuildValue("(s)", commit.text));
  if (!RimeFreeCommit(&commit)) {
    PyErr_SetString(PyExc_ValueError, "failed to free commit");
  }
  return commit_obj;
}

static PyObject *commitComposition(PyObject *self, PyObject *args) {
  RimeSessionId session_id;
  if (!PyArg_ParseTuple(args, "k|", &session_id))
    return NULL;
  return PyBool_FromLong(RimeCommitComposition(session_id));
}

static PyObject *clearComposition(PyObject *self, PyObject *args) {
  RimeSessionId session_id;
  if (!PyArg_ParseTuple(args, "k|", &session_id))
    return NULL;
  RimeClearComposition(session_id);
  Py_RETURN_NONE;
}

static PyMethodDef methods[] = {
    {"init", (PyCFunction)init, METH_VARARGS | METH_KEYWORDS, NULL},
    {"createSession", (PyCFunction)createSession, METH_NOARGS, NULL},
    {"destroySession", (PyCFunction)destroySession, METH_VARARGS, NULL},
    {"getCurrentSchema", (PyCFunction)getCurrentSchema, METH_VARARGS, NULL},
    {"getSchemaList", (PyCFunction)getSchemaList, METH_NOARGS, NULL},
    {"selectSchema", (PyCFunction)selectSchema, METH_VARARGS, NULL},
    {"processKey", (PyCFunction)processKey, METH_VARARGS, NULL},
    {"getContext", (PyCFunction)getContext, METH_VARARGS, NULL},
    {"getCommit", (PyCFunction)getCommit, METH_VARARGS, NULL},
    {"commitComposition", (PyCFunction)commitComposition, METH_VARARGS, NULL},
    {"clearComposition", (PyCFunction)clearComposition, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "pyrime", NULL, -1, methods,
};

PyMODINIT_FUNC PyInit_pyrime(void) {
  PyObject *m = PyModule_Create(&module);
  PyModule_AddStringConstant(m, "__version__", PROJECT_VERSION);
  PYMODULE_ADDOBJECT(m, Composition);
  PYMODULE_ADDOBJECT(m, Candidate);
  PYMODULE_ADDOBJECT(m, Menu);
  PYMODULE_ADDOBJECT(m, Context);
  PYMODULE_ADDOBJECT(m, Commit);
  PYMODULE_ADDOBJECT(m, SchemaListItem);
  return m;
}
