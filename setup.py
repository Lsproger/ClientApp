from cx_Freeze import setup, Executable

executables = [Executable('Main.py',
                          targetName='Cryptor.exe',
                          base='Win32GUI')]

zip_include_packages = ['collections', 'encodings', 'importlib', 'QApplication']

options = {
    'build_exe': {
        'include_msvcr': True,
        'zip_include_packages': zip_include_packages,
        'build_exe': 'BUILD',
    }
}

setup(name='Cryptor',
      version='0.0.12',
      description='Cryptor on elliptic curves',
      executables=executables,
      options=options,
      requires=['cx_Freeze', 'PyQt5', 'pbkdf2', 'Crypto'])
