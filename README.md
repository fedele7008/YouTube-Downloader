# YouTube-Downloader
Simple YouTube video downloader project

# Preview
<img width="1312" alt="Youtube-Downloader-preview" src="https://github.com/user-attachments/assets/8141b675-28da-4d96-ad1b-326b9598ce19">


# How to build for MacOS
1. Create a virtual environment
1. Activate the virtual environment
1. Install the dependencies `pip install -r requirements.txt`
1. Run `pyi-makespec --onefile --windowed src/main.py` from project root
1. Edit the spec file to following
```
# -*- mode: python ; coding: utf-8 -*-

import sys
import os

def get_requirements():
    with open('requirements.txt', 'r') as f:
        return [line.strip().split('==')[0] for line in f if line.strip() and not line.startswith('#')]

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[
        ('bin/mac/*', 'ffmpeg')
    ],
    datas=[
        ('src/assets', 'src/assets'),  # assets 폴더 전체를 포함
    ],
    hiddenimports=get_requirements(),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
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
    icon='icon/YoutubeDownloader.icns',  # macOS용 아이콘 경로
)

app = BUNDLE(
    exe,
    name='YouTube Downloader.app',
    icon='icon/YoutubeDownloader.icns',
    bundle_identifier='com.yourdomain.youtubedownloader',  # 번들 식별자 추가
)
```
1. Run `pyinstaller main.spec` from project root
1. Copy or Move `dist/Youtube Downloader.app` to `/Applications/`
