* Get the latest source

```
git pull
```

* If necesary, bump the version in `inselect/__init__.py`

* If the toolbar icons in inselect/data change then you need to refresh a Python
  file:

```
pyside-rcc icons.qrc > inselect/gui/icons.py
git commit -m "Refreshed icons" inselect/gui/icons.py
git push origin master
```

This taken from a [stackoverflow thread](http://stackoverflow.com/a/11547144)

* Check everything into git and `git push origin master`
* Build the Python package and Mac OS X installer:

```
cd ~/projects/inselect
git pull
./build.sh
```

* Build the Windows 64-bit Installer; start an Anaconda64 prompt:

```
cd c:\Users\<you Windows username>\projects\inselect
build.bat
```

* Archive `dist\inselect-0.1.18-amd64.msi`

* A [bug with `cx_Freeze`](https://github.com/NaturalHistoryMuseum/inselect/issues/130)
  means that we must maintain a patched `library.zip` for
  each Windows build, to be made available to any users who use the Inlight
  ClearImage barcode reading SDK.

    * Open `build\exe.win-amd64-2.7\library.zip` in Explorer

    * Navigate to `win32com\gen_py`

    * Open `C:\Users\Lawrence\Anaconda64\Lib\site-packages\win32com\gen_py` in
      explorer

    * Copy `F2BCF178-0B27-11D4-B5F5-9CC767000000x0x1x0` and `dicts.dat` to
    `library.zip\win32com\gen_py`

    * Close `build\exe.win-amd64-2.7\library.zip`

    * Archive `build\exe.win-amd64-2.7\library.zip` alongside the installer, in
      a folder called `Issue130Fix-64`


* Build the Windows 32-bit Installer; start an Anaconda32 prompt:

```
cd c:\Users\<you Windows username>\projects\inselect
git pull
build.bat
```

* Archive `dist\inselect-0.1.18-win32.msi`

* A [bug with `cx_Freeze`](https://github.com/NaturalHistoryMuseum/inselect/issues/130)
  means that we must maintain a patched `library.zip` for
  each Windows build, to be made available to any users who use the Inlight
  ClearImage barcode reading SDK.

    * Open `build\exe.win32-2.7\library.zip` in Explorer

    * Navigate to `win32com\gen_py`

    * Open `C:\Users\Lawrence\Anaconda32\Lib\site-packages\win32com\gen_py` in
      explorer

    * Copy `F2BCF178-0B27-11D4-B5F5-9CC767000000x0x1x0` and `dicts.dat` to
    `library.zip\win32com\gen_py`

    * Close `build\exe.win32-2.7\library.zip`

    * Archive `build\exe.win32-2.7\library.zip` alongside the installer, in
      a folder called `Issue130Fix-32`

* Tag

```
git tag -a -m v0.1.18 v0.1.18
git push origin master --tags
```

* Draft a new release on
  [the Inselect github releases page](https://github.com/NaturalHistoryMuseum/inselect/releases)
  and upload the installers.
