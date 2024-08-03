py = import('python').find_installation(pure: false)
rime_dep = dependency('rime')

py.extension_module(
  '__init__',
  '__init__.c',
  dependencies: [rime_dep],
  subdir: 'pyrime',
  install: true,
)
py.install_sources(
  ['__init__.pyi', '__main__.py', 'prompt_toolkit.py', 'parse_key.py', 'draw_ui.py'],
  subdir: 'pyrime',
)
py.install_sources(
  ['assets/json/keys.json', 'assets/json/modifiers.json'],
  subdir: 'pyrime/assets/json',
)
