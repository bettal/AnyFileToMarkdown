# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

markitdown_datas, markitdown_binaries, markitdown_hidden = collect_all('markitdown')
pyqt6_datas, pyqt6_binaries, pyqt6_hidden = collect_all('PyQt6')

a = Analysis(
    ['anyfile_to_markdown/app.py'],
    pathex=['.'],
    binaries=markitdown_binaries + pyqt6_binaries,
    datas=[
        ('icons/hicolor/256x256/apps/anyfile-to-markdown.png', 'icons'),
    ] + markitdown_datas + pyqt6_datas,
    hiddenimports=[
        'markitdown',
        'markitdown.converters',
    ] + markitdown_hidden + pyqt6_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'PyQt5',
        'PySide2',
        'PySide6',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AnyFileToMarkdown',
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
    icon='icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AnyFileToMarkdown',
)
