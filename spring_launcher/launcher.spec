# -*- mode: python -*-

block_cipher = None


##### include mydir in distribution #######
def extra_datas(mydir, norecurse=False):
    def rec_glob(p, files, norecurse):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            if not norecurse:
                rec_glob("%s/*" % d, files, norecurse)
    files = []
    rec_glob("%s/*" % mydir, files, norecurse)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas

import os
dirName = "."

a = Analysis(['launcher.py'],
             pathex=[os.path.join(dirName)],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt5.uic.plugins'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

print(a.datas)
a.datas += extra_datas(".", norecurse=True)
if os.path.isfile("exts"): # Add extensions if they exist
    a.datas += extra_datas("./exts")
a.datas += extra_datas("./unitsync")
a.datas += extra_datas("./bin")
print(a.datas)


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='launcher',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='launcher')
