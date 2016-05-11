* Get the latest source

```
git pull
```

* If necesary, bump the version in `inselect/__init__.py`

* If the icons in inselect/data change then you need to refresh a Python
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

* Build the Windows 64-bit Installer; start a Miniconda64 prompt:

```
cd c:\Users\<you Windows username>\projects\inselect
git pull
build.bat
```

* Archive `dist\inselect-0.1.18-amd64.msi`

* Build the Windows 32-bit Installer; start an Miniconda32 prompt:

```
cd c:\Users\<you Windows username>\projects\inselect
git pull
build.bat
```

* Archive `dist\inselect-0.1.18-win32.msi`

* Tag

```
git tag -a -m v0.1.18 v0.1.18
git push origin master --tags
```

* Draft a new release on
  [the Inselect github releases page](https://github.com/NaturalHistoryMuseum/inselect/releases)
  and upload the installers.
