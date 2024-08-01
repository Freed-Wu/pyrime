/**
 * #define PY_MEMBER_Foo(name) PY_MEMBER(Foo, name)
 * PY_NEW_OBJECT(Foo, foo, bar)
 *
 * class Foo:
 *     def __new__(cls, *a, **kw):
 *         foo_obj = object.__new__(cls)
 *         return foo_obj
 *
 *     def __init__(self, foo, bar):
 *         self.foo = foo
 *         self.bar = bar
 */
#ifndef __INIT___H
#define __INIT___H 1
#include <Python.h>
#include <structmember.h>

#include "for.h"

#define PY_OBJECT(name) PyObject *name;
#define PY_XDECREF(name) Py_XDECREF(self->name);
#define PY_SET_MEMBER(name)                                                    \
  if (name) {                                                                  \
    ptr = self->name;                                                          \
    Py_INCREF(name);                                                           \
    self->name = name;                                                         \
    Py_XDECREF(ptr);                                                           \
  }
#define PY_MEMBER(object_name, name)                                           \
  {#name, T_OBJECT_EX, offsetof(object_name, name), 0, NULL},
#define PY_NULL(name) *name = NULL,
#define KEYWORD(name) #name,
#define AND(name) &name,
#define PY_SELF(name) , self->name
#define PY_R(name) #name "=%R, "
#define PY_O(name) "O"

#define PY_NEW_OBJECT(object_name, ...)                                        \
  typedef struct {                                                             \
    PyObject_HEAD FOR(PY_OBJECT, __VA_ARGS__)                                  \
  } object_name;                                                               \
                                                                               \
  static void object_name##_dealloc(object_name *self) {                       \
    FOR(PY_XDECREF, __VA_ARGS__)                                               \
    Py_TYPE(self)->tp_free((PyObject *)self);                                  \
  }                                                                            \
                                                                               \
  static PyObject *object_name##_new(PyTypeObject *type, PyObject *args,       \
                                     PyObject *kw) {                           \
    int rc = -1;                                                               \
    object_name *self = NULL;                                                  \
    self = (object_name *)type->tp_alloc(type, 0);                             \
                                                                               \
    if (!self)                                                                 \
      goto error;                                                              \
                                                                               \
    rc = 0;                                                                    \
  error:                                                                       \
    if (rc < 0) {                                                              \
      FOR(PY_XDECREF, __VA_ARGS__)                                             \
      Py_XDECREF(self);                                                        \
    }                                                                          \
    return (PyObject *)self;                                                   \
  }                                                                            \
                                                                               \
  static int object_name##_init(object_name *self, PyObject *args,             \
                                PyObject *kw) {                                \
    int rc = -1;                                                               \
    static char *keywords[] = {FOR(KEYWORD, __VA_ARGS__) NULL};                \
    PyObject FOR(PY_NULL, __VA_ARGS__) *ptr = NULL;                            \
                                                                               \
    if (!PyArg_ParseTupleAndKeywords(args, kw, "|" FOR(PY_O, __VA_ARGS__),     \
                                     keywords, FOR(AND, __VA_ARGS__) NULL)) {  \
      goto error;                                                              \
    }                                                                          \
                                                                               \
    FOR(PY_SET_MEMBER, __VA_ARGS__)                                            \
    rc = 0;                                                                    \
  error:                                                                       \
    return rc;                                                                 \
  }                                                                            \
  static PyObject *object_name##_repr(object_name *self) {                     \
    return PyUnicode_FromFormat(#object_name "(" FOR(                          \
        PY_R, __VA_ARGS__) "extra=None)" FOR(PY_SELF, __VA_ARGS__));           \
  }                                                                            \
                                                                               \
  static PyMemberDef object_name##_members[] = {                               \
      FOR(PY_MEMBER_##object_name, __VA_ARGS__)};                              \
                                                                               \
  static PyMethodDef object_name##_methods[] = {{NULL, NULL, 0, NULL}};        \
                                                                               \
  static PyTypeObject object_name##Type = {                                    \
      PyVarObject_HEAD_INIT(NULL, 0).tp_name = "rime." #object_name,           \
      .tp_doc = #object_name,                                                  \
      .tp_basicsize = sizeof(object_name),                                     \
      .tp_itemsize = 0,                                                        \
      .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,                    \
      .tp_new = object_name##_new,                                             \
      .tp_init = (initproc)object_name##_init,                                 \
      .tp_dealloc = (destructor)object_name##_dealloc,                         \
      .tp_members = object_name##_members,                                     \
      .tp_repr = (reprfunc)object_name##_repr,                                 \
      .tp_methods = object_name##_methods};

#define PYMODULE_ADDOBJECT(m, object_name)                                     \
  do {                                                                         \
    if (PyType_Ready(&object_name##Type) < 0)                                  \
      return NULL;                                                             \
    PyModule_AddObject(m, #object_name, (PyObject *)&object_name##Type);       \
  } while (0)

#endif /* __init__.h */
