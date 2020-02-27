# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

agnostics_dir = os.path.join(os.getcwd(), "CGAgnostics")
icons_dir = os.path.join(os.getcwd(), 'transcoding', "toolkit", "icons")

a = Analysis([os.path.join(os.getcwd(), "transcoding", "toolkit", "__init__.py")],
             pathex=['C://Projects//CGToolkits//'],
             binaries=[],
             datas=[
                 ('./transcoding/ffmpeg', 'ffmpeg'),
                 (icons_dir, 'icons')
                 ],
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
          name='transcoding',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='transcoding')
