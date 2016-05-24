REM Temporary solution until I get round to writing a makefile

echo Building Inselect

echo Clean
del /S *pyc
rmdir /Q /S dist build 

echo Tests
nosetests --with-coverage --cover-html --cover-inclusive --cover-erase --cover-tests --cover-package=inselect inselect

echo Freeze stylesheet
python -m bin.freeze_stylesheet

echo Building MSI
python -m bin.com_clients
python setup.py bdist_msi
