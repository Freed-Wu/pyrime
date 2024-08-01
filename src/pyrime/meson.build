py = import('python').find_installation(pure: false)

py.extension_module(
  '__init__',
  '__init__.c',
  subdir: 'pyrime',
  install: true,
)
py.install_sources(
  ['prompt_toolkit.py'],
  subdir: 'pyrime',
)
