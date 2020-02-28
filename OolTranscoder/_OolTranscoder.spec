# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

agnostics_dir = os.path.join(os.getcwd(), "CGAgnostics")
icons_dir = os.path.join(os.getcwd(), "icons")

a = Analysis(["toolkit.py"],
             pathex=['C://Projects//CGToolkits//OolTranscoder'],
             binaries=[],
             datas=[
                 ('./ffmpeg', 'ffmpeg'),
                 (icons_dir, 'icons'),
                 (os.path.join(agnostics_dir, "icons"), "CGAgnostics/icons")
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
          name='OolTranscoder',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='icons\\video.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='OolTranscoder')
