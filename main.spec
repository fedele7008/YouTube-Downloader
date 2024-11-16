# -*- mode: python ; coding: utf-8 -*-
# Created from base of `pyi-makespec --onefile --windowed src/main.py --add-data src/youtube_downloader/resources:resources --add-binary src/youtube_downloader/external:external --icon src/youtube_downloader/resources/icon/YoutubeDownloader.icns --name "YouTube Downloader"`

import sys

if sys.platform == 'darwin':
    icon = 'src/youtube_downloader/resources/icon/YoutubeDownloader.icns'
elif sys.platform == 'win32':
    icon = 'src/youtube_downloader/resources/icon/YoutubeDownloader.ico'
else:
    icon = 'src/youtube_downloader/resources/icon/YoutubeDownloader.jpg'

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[('src/youtube_downloader/external', 'external')],
    datas=[('src/youtube_downloader/resources', 'resources')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='YouTube Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[icon],
)
app = BUNDLE(
    exe,
    name='YouTube Downloader.app',
    icon=icon,
    bundle_identifier=None,
)
