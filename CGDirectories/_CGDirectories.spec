# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['toolkit.py'],
             pathex=['C:\\Projects\\CGToolkits\\CGDirectories'],
             binaries=[],
             datas=[
                 ('docs/*.html', '.'),
                 ('icons/*.ico', 'icons'), 
                 ('components/icons/*.ico', 'components/icons'),
                 ('CGAgnostics/icons/*.ico', 'GCAgnostics/icons'),
                 ('config/*.json', 'config')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='CGDirectories',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='icons\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='CGDirectories')