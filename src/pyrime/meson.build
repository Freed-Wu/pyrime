py = import('python').find_installation(pure: false)
rime_dep = dependency('rime')

conf_data = configuration_data()
conf_data.set_quoted(
  'PROJECT_VERSION',
  meson.project_version(),
  description: 'project version',
)
conf_file = configure_file(output: 'config.h', configuration: conf_data)

py.extension_module(
  '__init__',
  ['__init__.c', conf_file],
  dependencies: [rime_dep],
  subdir: 'pyrime',
  install: true,
)
py.install_sources(
  [
    '__init__.pyi',
    '__main__.py',
    'parse_key.py',
    'draw_ui.py',
  ],
  subdir: 'pyrime',
)
py.install_sources(
  [
    'prompt_toolkit/__init__.py',
  ],
  subdir: 'pyrime/prompt_toolkit',
)
py.install_sources(
  [
    'prompt_toolkit/utils/condition.py',
    'prompt_toolkit/utils/ansi.py',
    'prompt_toolkit/utils/insert.py',
    'prompt_toolkit/utils/prompt_style.py',
  ],
  subdir: 'pyrime/prompt_toolkit/utils',
)
py.install_sources(
  [
    'prompt_toolkit/plugins/autopair.py',
    'prompt_toolkit/plugins/autosuggestion.py',
    'prompt_toolkit/plugins/smartinput.py',
    'prompt_toolkit/plugins/viemacs.py',
  ],
  subdir: 'pyrime/prompt_toolkit/plugins',
)
py.install_sources(
  ['assets/json/keys.json', 'assets/json/modifiers.json'],
  subdir: 'pyrime/assets/json',
)
