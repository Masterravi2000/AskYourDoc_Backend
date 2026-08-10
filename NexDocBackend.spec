# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

torch_datas, torch_binaries, torch_hiddenimports = collect_all("torch")
st_datas, st_binaries, st_hiddenimports = collect_all("sentence_transformers")
tf_datas, tf_binaries, tf_hiddenimports = collect_all("transformers")

a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=torch_binaries + st_binaries + tf_binaries,
    datas=[
    ('tesseract', 'tesseract'),
    ('models/all-MiniLM-L12-v2', 'models/all-MiniLM-L12-v2'),
    ('docs', 'docs'),
    ('NexDoc_DB', 'NexDoc_DB'),
    ('app/database/nexdoc.db', 'app/database'),
    *torch_datas,
    *st_datas,
    *tf_datas,
    ],
    hiddenimports=torch_hiddenimports + st_hiddenimports + tf_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='NexDocBackend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='NexDocBackend',
)
