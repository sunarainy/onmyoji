# -*- mode: python -*-

block_cipher = None

a = Analysis(['onmyoji_win.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('image/win10.png', '.\\image\\win10.png',  'DATA'),
('image/win7.png','.\\image\\win7.png','DATA'),
('image/single.png', '.\\image\\single.png',  'DATA'),
('image/passenger_accept.png', '.\\image\\passenger_accept.png',  'DATA'),
('image/driver_invite.png', '.\\image\\driver_invite.png',  'DATA'),
('image/driver_form.png', '.\\image\\driver_form.png',  'DATA'),
('senbonzakura.mid', '.\\senbonzakura.mid',  'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='onmyoji_win',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
