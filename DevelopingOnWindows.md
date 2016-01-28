# Windows development environment

Windows is complicated by the fact that we provide both 32-bit and 64-bit builds
of Inselect

# Install Miniconda 64 bit
* Download and run [Miniconda-latest-Windows-x86_64.exe](https://repo.continuum.io/miniconda/)

    * Destination folder should be called Miniconda64
    * Uncheck 'Add Miniconda to my PATH'

## Minicoda64 shortcut

I find it useful to have a shortcut on the desktop and taskbar, configured as
follows:

    * Target: `C:\Windows\System32\cmd.exe /k "C:\Users\<your Windows username>\Miniconda64\Scripts\activate.bat"`
    * Name Miniconda64
    * Start in: `C:\Users\<your Windows username>\`
    * Font: Consolas, 16
    * Layout: Buffer size, Width: 140
    * Layout: Window size, Width: 140

## Inselect environment

```
conda update --yes conda
conda create --yes --name inselect pillow pyside pywin32 numpy
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements.win64
FOR /F %a IN ('python -c "import sys; print(sys.exec_prefix)"') DO %a\python %a\Scripts\pywin32_postinstall.py -install
```

## Install OpenCV
* Download [OpenCV 2.4.11](http://opencv.org/)
* Extract OpenCV to `c:\opencv\`
* Copy the 64-bit extension module to the Anaconda64 environment:

    ```
    FOR /F %a IN ('python -c "import sys; print(sys.exec_prefix)"') DO copy C:\opencv\build\python\2.7\x64\cv2.pyd %a\DLLs
    ```

* Test

    ```
    python -c "import cv2; print cv2"
    ```

### Inlite barcode reading library
Download and install the [Inlite ClearImage SDK](http://www.inliteresearch.com/).

## Test barcode reading libraries

Inselect has optional barcode reading capabilities. The dependent libraries
should have been installed.

```
python -c "from gouda.engines import LibDMTXEngine; print(LibDMTXEngine.available())"
python -c "from gouda.engines import ZbarEngine; print(ZbarEngine.available())"
python -c "from gouda.engines import InliteEngine; print(InliteEngine.available())"
```

## Build

```
build.sh
```

Installer will be in `dist`.

# Install Miniconda 32 bit
* Download and run [Miniconda-latest-Windows-x86.exe](https://repo.continuum.io/miniconda/)
    * Destination folder should be called Miniconda32
    * Uncheck 'Add Anaconda to my PATH'

## Miniconda32 shortcut

I find it useful to have a shortcut on the desktop and taskbar, configured as
follows:

    * Target: `C:\Windows\System32\cmd.exe /k "C:\Users\<your Windows username>\Miniconda32\Scripts\activate.bat"`
    * Name Miniconda32
    * Start in: `C:\Users\<your Windows username>\`
    * Font: Consolas, 16
    * Layout: Buffer size, Width: 140
    * Layout: Window size, Width: 140

## Inselect environment

```
conda update --yes conda
conda create --yes --name inselect pillow pyside pywin32 numpy
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements.win64
FOR /F %a IN ('python -c "import sys; print(sys.exec_prefix)"') DO %a\python %a\Scripts\pywin32_postinstall.py -install
```

## Install OpenCV
* If you have not already done so for the 64-bit environment, download 
  [OpenCV 2.4.11](http://opencv.org/) and extract to `c:\opencv\`
* Copy the 32-bit extension module to the Anaconda32 environment:

    ```
    FOR /F %a IN ('python -c "import sys; print(sys.exec_prefix)"') DO copy C:\opencv\build\python\2.7\x86\cv2.pyd %a\DLLs
    ```

* Test

    ```
    python -c "import cv2; print cv2"
    ```

### Inlite barcode reading library
If you have not already done so for the 64-bit environment, download and install
the [Inlite ClearImage SDK](http://www.inliteresearch.com/).

## Test barcode reading libraries

Inselect has optional barcode reading capabilities. The dependent libraries
should have been installed.

```
python -c "from gouda.engines import LibDMTXEngine; print(LibDMTXEngine.available())"
python -c "from gouda.engines import ZbarEngine; print(ZbarEngine.available())"
python -c "from gouda.engines import InliteEngine; print(InliteEngine.available())"
```

## Build

```
build.sh
```

Installer will be in `dist`.

