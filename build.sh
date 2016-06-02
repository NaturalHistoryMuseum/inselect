# Temporary solution until I get round to writing a makefile

set -e  # Exit on failure

VERSION=`python inselect.py --version 2>&1 | sed 's/inselect.py //g'`

echo Building Inselect $VERSION

echo Clean
rm -rf cover build dist
find . -name "*pyc" -print0 | xargs -0 rm -rf
find . -name __pycache__ -print0 | xargs -0 rm -rf

echo Freeze icons
python -m bin.freeze_icons

echo Tests
nosetests --with-coverage --cover-html --cover-inclusive --cover-erase --cover-tests --cover-package=inselect inselect

echo Report startup time and check for non-essential binary imports
mkdir build
time python -v inselect.py --quit &> build/startup_log
for module in cv2 numpy pydmtx scipy sklearn zbar; do
    if grep -q $module build/startup_log; then
        echo Non-essential binary $module imported on startup
        exit 1
    fi
done

echo Source build
./setup.py sdist
mv dist/inselect-$VERSION.tar.gz .

if [[ "$OSTYPE" == "darwin"* ]]; then
    # Clean existing build files
    pyinstaller --clean inselect.spec

    for script in export_metadata ingest read_barcodes save_crops; do
        rm -rf $script.spec
        pyinstaller --onefile --hidden-import numpy inselect/scripts/$script.py
    done
    # segment has an additional hidden import
    rm -rf segment.spec
    pyinstaller --onefile --hidden-import numpy \
        --hidden-import sklearn.neighbors.typedefs inselect/scripts/segment.py

    # Add a few items to the PropertyList file generated by PyInstaller
    python -m bin.plist dist/inselect.app/Contents/Info.plist
    # Example document
    install -c -m 644 examples/Plecoptera_Accession_Drawer_4.jpg dist/
    install -c -m 644 examples/Plecoptera_Accession_Drawer_4.inselect dist/
    # Remove the directory containing the console app (the windowed app is in inselect.app)
    rm -rf dist/inselect
    rm -rf inselect-$VERSION.dmg
    hdiutil create inselect-$VERSION.dmg -volname inselect-$VERSION -srcfolder dist
fi
