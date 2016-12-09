REM Temporary solution until I get round to writing a makefile

echo Building Inselect

echo Clean
del /S *pyc
rmdir /Q /S dist build

echo Freeze icons
pyrcc5 icons.qrc > inselect/gui/icons.py || exit /b

echo Check for presence of barcode engines
python -c "from gouda.engines import ZbarEngine; assert ZbarEngine.available()" || exit /b
python -c "from gouda.engines import LibDMTXEngine; assert LibDMTXEngine.available()" || exit /b
python -c "from gouda.engines import InliteEngine; assert InliteEngine.available()" || exit /b

echo Tests
nosetests --with-coverage --cover-html --cover-inclusive --cover-erase --cover-tests --cover-package=inselect inselect || exit /b

echo Building MSI
python -m bin.com_clients || exit /b
python setup.py bdist_msi || exit /b
