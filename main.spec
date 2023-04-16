# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/main.py'],
    pathex=[],
    binaries=[],
    datas=[('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/constants.py', '.'), ('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/credit.txt', '.'), ('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/level_data.csv', '.'), ('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/musicplayer.py', '.'), ('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/player.py', '.'), ('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/render.py', '.'), ('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/timer.py', '.'), ('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/tutorial_data.csv', '.'), ('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/utils.py', '.'), ('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/world_map.py', '.'), ('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2', 'ten-second-time2/'), ('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2', 'ten-second-time2/'), ('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/assets', 'assets/'), ('/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/powerups', 'powerups/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='/mnt/c/Users/micah/Documents/GitHub/ten-second-time2/assets/icon.ico',
)
