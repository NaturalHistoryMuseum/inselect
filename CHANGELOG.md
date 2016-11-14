This is an overview of major changes. Refer to the git repository for a full log change.

Version 0.1.35
-------------
- #377 Windows non-latin username test
- #374 Support pyzbar
- #372 Support pydmtxlib
- #368 Ugly error message when creating a new inselect document on Mac OS X
- #273 Inselect as a package
- #83 Architecture and code organisation

Version 0.1.34
-------------
- #362 Command-line option to print elapsed time for which document was open

Version 0.1.34
-------------
- #353 Error 5
- #351 Metadata templates to allow fields with fixed values
- #349 Linux instructions
- #347 Explicitly reference python2 in scripts
- #342 Conda environment files
- #331 Box resize doing crazy things - emergency fix: restrict max zoom level
- #333 Ugly error message when opening or saving a file
- #332 Error when saving crops in Dropbox folder
- #330 libdmtx URL incorrect
- #328 Menu commands to show cookie cutter and metadata template files
- #325 Command-line option to set window size

Version 0.1.33
-------------
- #322 Build scripts to check that barcode readers are available
- #320 Some view menu items missing from keyboard shortcuts box

Version 0.1.32
-------------
- #315 Ribbon
- #207 Help for hotkeys

Version 0.1.31
-------------
- #307 Test performance
- #305 Remove references to 'scanned image'
- #210 Improve UI design

Version 0.1.30
-------------
- #303 Improve startup time

Version 0.1.29
-------------
- #298 Ugly error message when double-clicking on a .inselect file
- #296 Inconsistent zoom toggling
- #295 Full-resolution scan is mandatory
- #293 Link to files fails with ugly error message on Windows
- #131 Main window icon

Version 0.1.28
-------------
- #291 Alter travis to use Anaconda / Miniconda
- #288 Minimap navigator
- #286 Disable default template command when the default template selected
- #284 Document info view to contain links
- #281 Don't make images read-only
- #212 Customized bounding box ordering
- #204 Improvements to subsegment dots
- #203 Resize handles should have constant size regardless of zoom

Version 0.1.27
-------------
- #277 Subsegment box broken
- #275 Test image has executable bit set (@edwbaker)

Version 0.1.26
-------------
- #263 Subsegment box should copy metadata to new boxes
- #262 Scripts to respect keyboard interrupt (CTRL + C)
- #258 CTRL / apple key + number to select the active view
- #256 Disable template 'Reload' command when default template selected
- #254 An Error Occurred: {'Choices with data ...
- #218 N boxes / N selected widget to a status bar
- #213 Increase default border around "objects" post segmentation

Version 0.1.25
-------------
- #249 Better handling of multiple and unrecognised metadata values
- #248 Better default text in Cookie Cutter dropdown
- #247 Locations of bounding boxes in CSV
- #243 Template validation when value is not in drop-down list of values
- #242 Unnecessary second read of full-res image after creating new document

Version 0.1.24
-------------
- #240 Objects view - better object labels
- #237 Ugly error message when opening document on Mac OS X
- #236 Reset zoom mode when opening new document

Version 0.1.23
-------------
- #234 Metadata template popup (@quicklizard99)
- #233 Error box should contain traceback (@quicklizard99)
- #230 No way to for the user to specify thumbnail size to the ingest command-line tool (@quicklizard99)
- #228 Closing document can be slow (@quicklizard99)
- #217 Error box appears twice (@quicklizard99)

Version 0.1.22
-------------
- #225 Mac command-line tools are broken (@quicklizard99)
- #219 Command-line tools to use metadata and cookie-cutter templates (@quicklizard99)

Version 0.1.21
-------------
- #208 Thousands separators for N boxes and N selected boxes (@quicklizard99)
- #205 A 'Reload template' button (@quicklizard99)
- #198 Opening both .inselect files and images by drag-drop is broken (@quicklizard99)
- #192 Cookie cutter templates (@quicklizard99)
- #176 workflow to scripts (@quicklizard99)
- #48 Zooming should follow mouse position (@quicklizard99)

Version 0.1.20
-------------
- #196 Change colour scheme does not refresh view on Windows (@quicklizard99)
- #193 Better logic when checking for duplicated metadata values (@quicklizard99)
- #190 read_barcodes.py to take choice of barcode engine on command line (@quicklizard99)
- #189 Include read_barcodes (@quicklizard99)
- #188 Choice of colour scheme not persisted (@quicklizard99)
- #184 Missing menu item ellipses (@quicklizard99)
- #183 Simple colour schemes (@quicklizard99)
- #182 Select by size (@quicklizard99)
- #181 Box adjustment keyboard shortcuts (@quicklizard99)
- #180 Next / previous box should zoom to fit (@quicklizard99)
- #179 Standard keyboard shortcuts to move between tabs (@quicklizard99)
- #155 Avoiding crop file name collisions (@quicklizard99)

Version 0.1.19
-------------
- #173 Mac build broken (@quicklizard99)

Version 0.1.18
-------------
- #130 Barcode reading broken in compiled Inselect on Windows (@quicklizard99)

Version 0.1.17
-------------
- #171 Processing double-sided objects (@quicklizard99)

Version 0.1.16
-------------
- #169 Better formatting of validation problems (@quicklizard99)

Version 0.1.15
-------------
- #167 Richer information in about box (@quicklizard99)
- #126 Recent documents (@quicklizard99)
- #168 Information panel shows incorrect file sizes (@quicklizard99)
- #166 Enter does not toggle Objects view between 'grid' and 'expanded' on Mac OS X (@quicklizard99)
- #134 Delete box should not scroll Metadata view (@quicklizard99)

Version 0.1.14
-------------
- #165 User templates to support thumbnail width pixels (@quicklizard99)

Version 0.1.13
-------------
- #156 User-defined project templates (@quicklizard99)
- #164 Cropped images not saved with rotation (@quicklizard99)
- #159 Unable to open jpegs with uppercase filename extension (@quicklizard99)
- #157 ingest workflow tool should ignore _thumbnail images (@quicklizard99)
- #151 'Save screen grab' should suggest a filename (@quicklizard99)
- #150 Support .bmp (@quicklizard99)
- #129 Warn when a read-only document is opened (@quicklizard99)
- #121 A menu option to save the boxes view to an image file (@quicklizard99)
- #120 Show information about the scanned image (@quicklizard99)
- #117 Bounding boxes can be created and moved outside of the image (@quicklizard99)
- #113 A shortcut for navigating between the Boxes and Metadata views (@quicklizard99)
- #94 Hard-coded keyboard shortcuts in help text (@quicklizard99)
- #88 Open-source Data Matrix, 1D barcode, and QR code decoding on all OSes (@quicklizard99)
- #82 CMD+backspace on OS X should delete selected boxes (@quicklizard99)

Version 0.1.12
-------------
*Natural History Museum internal release*
- #161 Free text metadata template (@quicklizard99)
- #160 Missing Macrosiphum locations (@quicklizard99)

Version 0.1.11
-------------
*Natural History Museum internal release*
- #159 Unable to open jpegs with uppercase filename extension (@quicklizard99)
- #157 ingest workflow tool should ignore _thumbnail images (@quicklizard99)
- #151 'Save screen grab' should suggest a filename (@quicklizard99)
- #150 Support .bmp (@quicklizard99)
- #129 Warn when a read-only document is opened (@quicklizard99)
- #113 A shortcut for navigating between the Boxes and Metadata views (@quicklizard99)
- #94 Hard-coded keyboard shortcuts in help text (@quicklizard99)
- #88 Open-source Data Matrix, 1D barcode, and QR code decoding on all OSes (@quicklizard99)
- #82 CMD+backspace on OS X should delete selected boxes (@quicklizard99)

Version 0.1.10
-------------
*Natural History Museum internal release*
- #149 Add metadata templates for Aphididae and Ephemeroptera enhancement (@quicklizard99)
- #148 Unable to create new boxes (@quicklizard99)

Version 0.1.9
-------------
*Natural History Museum internal release*
- #88 Open-source Data Matrix barcode decoding on Linux and Mac OS X (@quicklizard99)
- #116 Metadata templates and associated validation (@quicklizard99)
- #118 Rotation arrows on the metadata view do not appear correctly on Windows (@quicklizard99)

Version 0.1.8
-------------
*Natural History Museum internal release*
- #88 Open-source Data Matrix barcode decoding on Linux and Mac OS X (@quicklizard99)
- #116 Metadata templates and associated validation (@quicklizard99)
- #121 A menu option to save the boxes view to an image file (@quicklizard99)
- #120 Show information about the scanned image (@quicklizard99)
- #117 Bounding boxes can be created and moved outside of the image (@quicklizard99)

Version 0.1.7
-------------
- #138 Metadata fields to be available on boxes view (@quicklizard99)
- #137 Metadata title should not scroll with fields (@quicklizard99)
- #136 Reopening the currently open document is confusing (@quicklizard99)
- #133 Show proxy icon on Mac OS X (@quicklizard99)
- #132 Show modified state in title (@quicklizard99)
- #109 Larger images in metadata view (@quicklizard99)

Version 0.1.6
-------------
- #130 Broken barcode reading on Windows (@quicklizard99)
- #116 Metadata fields are Simple Darwin Core terms (@quicklizard99)
- #84 Tests (@quicklizard99)
- #127 .tif file extension not recognised (@quicklizard99)
- #125 Display issue on Windows: After startup, Window title, frame and controls out of screen (@quicklizard99)
- #124 "New" doesn't work if inselect document already exists (@quicklizard99)
- #119 Non-latin characters in 'Specimen number' metadata field causes grid item title to disappear (@quicklizard99)
- #115 Silly wording when a single box selected (@quicklizard99)
- #106 Select newly created bounding box (@quicklizard99)
- #104 File, Open versus File, New ambiguity (@quicklizard99)
- #87 Large images do not display correctly (@quicklizard99)
- #74 Mac OS X installer (@quicklizard99)

Version 0.1.5
-------------
- Icons for plugins (@quicklizard99)
- CSV export (@quicklizard99)
- Progress box during 'New document' (@quicklizard99)
- Open files via drag-drop (@quicklizard99)

Version 0.1.4
-------------
- Document format (@quicklizard99)
- Workflow tools (@quicklizard99)
- UI reimplementation (@quicklizard99)
- OS X (Mac) build (@quicklizard99)
- Myriad bug fixes and enhancements (@quicklizard99)
- Add license and changelog (@aliceh75)
- Added help dialog (@aliceh75)
- Add previous/next navigation in the annotation dialog (@aliceh75)
- Refactor code to separate UI and application logic (@aliceh75)
- Add padding option (@holtzhau)
- Improve segmentation by resizing image (@holtzhau)

Version 0.1.3
-------------
- Add persistent settings and settings dialog box (@aliceh75)
- Segmentation algorithm tweaks (@holtzhau)
- Added tiff image detection on export (@holtzhau)
- Make exported image name configurable via settings (@aliceh75)
- Refactor file structure to prepare for UI/application logic separation (@aliceh75)
- Refactor BoxResiable to use mouse events (@aliceh75)
- Fix box ordering on keyboar next/previous (@holtzhau)
- Remember open directory (@holtzhau)

Version 0.1.2
-------------
- Multiple object annotation (@holtzhau)
- Added key navigation to sidebar (@holtzhau)
- Various fixes (@holtzhau)

Version 0.1.1
-------------
- Added annotator dialog (@holtzhau)
- Switch from multiprocessing to QThreads (@holtzhau)
- Added display_image routine and elaborated on resegment (@holtzhau)
- Added sidebar (@holtzhau)
- Added importing and saving of boxes (@holtzhau)
- Use json for import/export (@holtzhau)
- Improvement to segmentation (@holtzhau)
- Added seed growing in segmentation and interface (@holtzhau)
- Key based navigation (@aliceh75)
- Refactor mouse event handling (@aliceh75)
- Add zoom with wheel (@aliceh75)

Version 0.1
-----------
- Initial test release (@stefanv, @holtzhau)
