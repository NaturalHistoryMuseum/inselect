# Temporary solution until I get round to writing a makefile

set -e  # Exit on failure

VERSION=`python inselect.py --version 2>&1 | sed 's/inselect.py //g'`

echo Building Inselect $VERSION

echo Clean
find . -name "*pyc" -print0 | xargs -0 rm -rf
find . -name __pycache__ -print0 | xargs -0 rm -rf
rm -rf *spec dist build cover inselect-$VERSION.dmg

echo Tests
nosetests --with-coverage --cover-html --cover-inclusive --cover-erase --cover-tests --cover-package=inselect

echo Source build
python setup.py sdist
mv dist/inselect-$VERSION.tar.gz .

if [[ "$OSTYPE" == "darwin"* ]]; then
    # Clean existing build files and dmg
    rm -rf dist build
    rm -rf inselect-$VERSION.dmg
    pyinstaller --onefile --windowed --icon=data/inselect.icns inselect.py
    pyinstaller --onefile --icon=data/inselect.icns inselect/workflow/export_metadata.py
    pyinstaller --onefile --icon=data/inselect.icns inselect/workflow/ingest.py
    pyinstaller --onefile --icon=data/inselect.icns inselect/workflow/save_crops.py
    pyinstaller --onefile --icon=data/inselect.icns inselect/workflow/segment.py
    ./bin/plist.py dist/inselect.app/Contents/Info.plist
    install -c -m 644 data/Plecoptera_Accession_Drawer_4.jpg dist/
    install -c -m 644 data/Plecoptera_Accession_Drawer_4.inselect dist/
    rm dist/inselect
    hdiutil create inselect-$VERSION.dmg -volname inselect-$VERSION -srcfolder dist
fi
