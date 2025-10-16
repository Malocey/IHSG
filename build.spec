# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import hookspath, runtime_hooks
from PyInstaller.utils.hooks import collect_data_files

# This file is a PyInstaller spec file. It tells PyInstaller how to build the executable.

# Analysis block: This part analyzes the project's source code to find all dependencies.
a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             # Collect all data files used by Kivy (e.g., default theme)
             datas=collect_data_files('kivy'),
             hiddenimports=[],
             # Add Kivy's specific hooks
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             hooksconfig={},
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None,
             noarchive=False)

# Add our game's assets to the bundle.
# This ensures that 'assets/hero.png', 'assets/enemy.png', etc., are included.
a.datas += [('assets/*', 'assets', 'DATA')]

# PY_Zipped_Archive block: This creates a zipped archive of all Python scripts.
pyz = PYZ(a.pure, a.zipped_data,
             cipher=None)

# Executable block: This defines the executable itself.
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='IdleHordeSlayer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          # The console=False option prevents a command prompt window from opening in the background.
          # Set to True for debugging purposes.
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          # Set an icon for the executable (optional).
          # You would need to create an 'icon.ico' file for this to work.
          # icon='assets/icon.ico'
          )