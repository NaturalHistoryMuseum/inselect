# Windows development environment

Windows is complicated by the fact that we provide both 32-bit and 64-bit builds
of Inselect

# Install git

Download and run the [latest Windows build of git](http://git-scm.com/download/win)

* Use git from command prompt
* Checkout as-is, commit as-is

Configure git:

```
git config --global user.name "<Your name>"
git config --global user.email <Your email address>
git config --global credential.helper wincred
```

# Install a sensible text editor

I use [Sublime Text](http://www.sublimetext.com/).

**Whatever you use, set your editor to use Unix line endings and to insert
spaces in place of TABs**.

# Code repos

Start a command prompt

```
cd C:\Users\<your Windows username>\
mkdir projects
cd projects
git clone https://<your git username>@github.com/NaturalHistoryMuseum/inselect.git
git clone https://<your git username>@github.com/NaturalHistoryMuseum/gouda.git
```

# Paths

In Advanced system settings create an environment variable:

```
PYTHONPATH=C:\Users\<your Windows username>\projects\inselect;C:\Users\<your Windows username>\projects\gouda;
```

# Install Anaconda 64 bit
* Download and run the latest build of
  [Anaconda](https://store.continuum.io/cshop/anaconda/) Python 2.7.x, 64-bit

    * Destination folder should be called Anaconda64
    * Uncheck 'Add Anaconda to my PATH'

* In your editor, open `C:\Users\<your Windows username>\Anaconda64\Scripts\anaconda.bat`
  and alter the line `title Anaconda` to `title Anaconda64`

## Anaconda64 shortcut

I find it useful to have a shortcut on the desktop and taskbar, configured as
follows:

    * Target: `C:\Windows\System32\cmd.exe /k "C:\Users\<your Windows username>\Anaconda64\Scripts\anaconda.bat"`
    * Start in: `C:\Users\<your Windows username>\Anaconda64`
    * Font: Consolas, 16

* Start an Anaconda64 prompt and run

```
conda update --all
conda update --all
conda update conda
conda update anaconda
pip install --upgrade pip
python %ANACONDA%\Scripts\pywin32_postinstall.py -install
```

## Install OpenCV
* Download the latest release of [OpenCV 2.x](http://opencv.org/)
* Extract OpenCV to c:\opencv\
* Copy the 64-bit extension module to the Anaconda64 environment:

```
copy C:\opencv\build\python\2.7\x64\cv2.pyd C:\Users\<your Windows username>\Anaconda64\DLLs`
```

* Test by starting Anaconda64 prompt and running

```
python -c "import cv2; print cv2"
```

## Install dependencies and useful tools

```
cd C:\Users\<your Windows username>\projects\
pip install nose Markdown
pip install cx_Freeze
conda install pyside
conda install Pillow
pip install -r inselect\requirements.txt
pip install -r gouda\requirements.txt
```

### Inlite barcode reading library
Download and install the [Inlite ClearImage SDK](http://www.inliteresearch.com/).

## LibDMTX barcode reading library
Download and install the 64-bit build of `pydmtx` from
[our dmtx-wrapper repo](https://github.com/NaturalHistoryMuseum/dmtx-wrappers/);
at the time of writing, this is
[pydmtx-0.7.4b1-cp27-none-win_amd64.whl](https://github.com/NaturalHistoryMuseum/dmtx-wrappers/releases)

    pip install pydmtx-0.7.4b1-cp27-none-win_amd64.whl

Test

    python -c "import pydmtx; print(pydmtx)"

## ZBar barcode reading library
Download and install the build from
[our ZBarWin64 repo](https://github.com/NaturalHistoryMuseum/ZBarWin64/); at the
time of writing, this is
[zbar-0.10-cp27-none-win_amd64.whl](https://github.com/NaturalHistoryMuseum/ZBarWin64/releases)

```
pip install zbar-0.10-cp27-none-win_amd64.whl
```

Test

```
python -c "import zbar; print(zbar)"
```

# Unit tests

```
cd C:\Users\<your Windows username>\projects\gouda
nosetests --with-coverage --cover-html --cover-inclusive --cover-erase --cover-tests --cover-package=gouda

cd C:\Users\<your Windows username>\projects\inselect
nosetests --with-coverage --cover-html --cover-inclusive --cover-erase --cover-tests --cover-package=inselect
```

# Install Anaconda 32 bit
* Download and run the latest build of
  [Anaconda](https://store.continuum.io/cshop/anaconda/) Python 2.7.x, 32-bit

    * Destination folder should be called Anaconda32
    * Uncheck 'Add Anaconda to my PATH'

* In your editor, open `C:\Users\<your Windows username>\Anaconda32\Scripts\anaconda.bat`
  and alter the line `title Anaconda` to `title Anaconda32`

## Anaconda32 shortcut

I find it useful to have a shortcut on the desktop and taskbar, configured as
follows:

    * Target: `C:\Windows\System32\cmd.exe /k "C:\Users\<your Windows username>\Anaconda32\Scripts\anaconda.bat"`
    * Start in: `C:\Users\<your Windows username>\Anaconda32`
    * Font: Consolas, 16

* Start and Anaconda32 prompt and run

```
conda update --all
conda update --all
conda update conda
conda update anaconda
pip install --upgrade pip
python %ANACONDA%\Scripts\pywin32_postinstall.py -install
```

## Install OpenCV
* If you have not already done so for the 64-bit environment, download the
  latest release of [OpenCV 2.x](http://opencv.org/) and extract to c:\opencv\
* Copy the 32-bit extension module to the Anaconda32 environment:

```
copy C:\opencv\build\python\2.7\x86\cv2.pyd C:\Users\<your Windows username>\Anaconda32\DLLs`
```

* Test by starting an Anaconda32 prompt and running

```
python -c "import cv2; print cv2"
```

## Install dependencies and useful tools

```
cd C:\Users\<your Windows username>\projects\
pip install nose Markdown
pip install cx_Freeze
conda install pyside
conda install Pillow
pip install -r inselect\requirements.txt
pip install -r gouda\requirements.txt
```

### Inlite barcode reading library
If you have not already done so for the 64-bit environment, download and install
the [Inlite ClearImage SDK](http://www.inliteresearch.com/).

## LibDMTX barcode reading library
Download and install the 64-bit build of `pydmtx` from
[our dmtx-wrapper repo](https://github.com/NaturalHistoryMuseum/dmtx-wrappers/);
at the time of writing, this is
[pydmtx-0.7.4b1-cp27-none-win32.whl](https://github.com/NaturalHistoryMuseum/dmtx-wrappers/releases)

```
pip install pydmtx-0.7.4b1-cp27-none-win32.whl
```

Test

```
python -c "import pydmtx; print(pydmtx)"
```

## ZBar barcode reading library
Building this from source requires you to install Microscoft Visual C and
some dependencies. I have made a build available at XXX. Download this and copy
to the Anaconda32 environment:

```
copy cv2.pyd C:\Users\<your Windows username>\Anaconda32\DLLs\`
```

Test

```
python -c "import zbar; print(zbar)"
```

# Unit tests

```
cd C:\Users\<your Windows username>\projects\gouda
nosetests --with-coverage --cover-html --cover-inclusive --cover-erase --cover-tests --cover-package=gouda

cd C:\Users\<your Windows username>\projects\inselect
nosetests --with-coverage --cover-html --cover-inclusive --cover-erase --cover-tests --cover-package=inselect
```
