# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:\\Users\\leo13\\Dropbox\\Programs\\LBRYchanneldownloader\\c.py'],
             pathex=['C:\\Users\\leo13\\Dropbox\\Programs\\LBRYchanneldownloader'],
             binaries=[],
             datas=[('C:\\Users\\leo13\\Dropbox\\Programs\\LBRYchanneldownloader\\lbrynet.exe', '.')],
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
          name='LbrySeed',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='C:\\Users\\leo13\\Dropbox\\Programs\\LBRYchanneldownloader\\a.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='LbrySeed')
