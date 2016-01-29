REM Temporary solution until I get round to writing a makefile

echo Building Inselect

echo Clean
del /S *pyc
del *spec
rmdir /Q /S dist build 

echo Tests
nosetests --with-coverage --cover-html --cover-inclusive --cover-erase --cover-tests --cover-package=inselect inselect

echo Building MSI
python -m bin.com_clients
python setup.py bdist_msi
