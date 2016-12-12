# Windows development environment

Windows is complicated by the fact that we provide both 32-bit and 64-bit builds
of Inselect

# Install Miniconda3 64 bit
* Download and run [Miniconda3-latest-Windows-x86_64.exe](https://repo.continuum.io/miniconda/)

    * Destination folder should be called Miniconda64
    * Uncheck 'Add Anaconda to my PATH'
    * Uncheck 'Register Anaconda as my default Python 2.7'

## Minicoda3-64 shortcut

I find it useful to have a shortcut on the desktop and taskbar, configured as
follows:

    * Target: `C:\Windows\System32\cmd.exe /k "C:\Users\<your Windows username>\Miniconda64\Scripts\activate.bat"`
    * Name Miniconda3-64
    * Start in: `C:\Users\<your Windows username>\`
    * Font: Consolas, 16
    * Layout: Buffer size, Width: 140
    * Layout: Window size, Width: 140


# Install Miniconda3 32 bit
* Download and run [Miniconda3-latest-Windows-x86.exe](https://repo.continuum.io/miniconda/)
    * Destination folder should be called Miniconda32-3
    * Uncheck 'Add Anaconda to my PATH'

## Miniconda3-32 shortcut

I find it useful to have a shortcut on the desktop and taskbar, configured as
follows:

    * Target: `C:\Windows\System32\cmd.exe /k "C:\Users\<your Windows username>\Miniconda32\Scripts\activate.bat"`
    * Name Miniconda3-32
    * Start in: `C:\Users\<your Windows username>\`
    * Font: Consolas, 16
    * Layout: Buffer size, Width: 140
    * Layout: Window size, Width: 140

# Instructions common to both 32-bit and 64-bit

You should run through these for both the 32-bit and 64-bit environments that
you created above.

## Inselect environment

```
conda update --yes conda
conda env create -f inselect.yml
activate inselect
conda install pywin32=220
FOR /F %a IN ('python -c "import sys; print(sys.exec_prefix)"') DO %a\python %a\Scripts\pywin32_postinstall.py -install
pip install -r requirements.pip
```

Don't worry about the "Can't install shortcuts..." message when you run the
`pywin32_postinstall` step.

### Inlite barcode reading library
Download and install the [Inlite ClearImage SDK](http://www.inliteresearch.com/).
Run the 'Inlite Control Center' application to get an evaluation key.

## Test barcode reading libraries

Inselect has optional barcode reading capabilities. The dependent libraries
should have been installed.

```
python -c "from gouda.engines import LibDMTXEngine; print(LibDMTXEngine.available())"
python -c "from gouda.engines import ZbarEngine; print(ZbarEngine.available())"
python -c "from gouda.engines import InliteEngine; print(InliteEngine.available())"
```

# Developing

Icons are stored as individual files in `icons`. They are frozen into
a python file `inselect/gui/icons.py` by running

```
pyrcc5 icons.qrc > inselect/gui/icons.py
```

# Test and run

```
nosetests --verbose --with-coverage --cover-inclusive --cover-tests --cover-package=inselect inselect
```

Run inselect

```
python -m inselect.scripts.inselect
```

# Build

The build script freezes icons, runs tests, freezes python and assembles files
into an installer.

```
build.bat
```

The installer will be in `dist`.
