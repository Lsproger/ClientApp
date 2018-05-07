from cx_Freeze import setup, Executable

executables = [Executable('Main.py',
                          targetName='MainApp.exe',
                          base='Win32GUI')]

zip_include_packages = ['collections', 'encodings', 'importlib', 'QApplication']

options = {
    'build_exe': {
        'include_msvcr': True,
        'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',
    }
}

setup(name='hello_world',
      version='0.0.12',
      description='My Hello World App!',
      executables=executables,
      options=options,
      requires=['cx_Freeze', 'PyQt5', 'pbkdf2', 'Crypto'])