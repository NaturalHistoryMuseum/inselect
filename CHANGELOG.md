This is an overview of major changes. Refer to the git repository for a full log change.

Version 0.1.19
-------------
- Fixed #173 - Mac build broken (@quicklizard99)

Version 0.1.18
-------------
- Fixed #130 - Barcode reading broken in compiled Inselect on Windows (@quicklizard99)

Version 0.1.17
-------------
- Added #171 - Processing double-sided objects (@quicklizard99)

Version 0.1.16
-------------
- Fixed #169 - Better formatting of validation problems (@quicklizard99)

Version 0.1.15
-------------
- Added #167 - Richer information in about box (@quicklizard99)
- Added #126 - Recent documents (@quicklizard99)
- Fixed #168 - Information panel shows incorrect file sizes (@quicklizard99)
- Fixed #166 - Enter does not toggle Objects view between 'grid' and 'expanded' on Mac OS X (@quicklizard99)
- Fixed #134 - Delete box should not scroll Metadata view (@quicklizard99)

Version 0.1.14
-------------
- Added #165 - User templates to support thumbnail width pixels (@quicklizard99)

Version 0.1.13
-------------
- Work on #156 - User-defined project templates (@quicklizard99)
- Fixed #164 - Cropped images not saved with rotation (@quicklizard99)
- Fixed #159 - Unable to open jpegs with uppercase filename extension (@quicklizard99)
- Fixed #157 - ingest workflow tool should ignore _thumbnail images (@quicklizard99)
- Fixed #151 - 'Save screen grab' should suggest a filename (@quicklizard99)
- Fixed #150 - Support .bmp (@quicklizard99)
- Fixed #129 - Warn when a read-only document is opened (@quicklizard99)
- Fixed #121 - A menu option to save the boxes view to an image file (@quicklizard99)
- Fixed #120 - Show information about the scanned image (@quicklizard99)
- Fixed #117 - Bounding boxes can be created and moved outside of the image (@quicklizard99)
- Fixed #113 - A shortcut for navigating between the Boxes and Metadata views (@quicklizard99)
- Fixed #94 - Hard-coded keyboard shortcuts in help text (@quicklizard99)
- Fixed #88 - Open-source Data Matrix, 1D barcode, and QR code decoding on all OSes (@quicklizard99)
- Fixed #82 - CMD+backspace on OS X should delete selected boxes (@quicklizard99)

Version 0.1.12
-------------
*Natural History Museum internal release*
- Fixed #161 - Free text metadata template (@quicklizard99)
- Fixed #160 - Missing Macrosiphum locations (@quicklizard99)

Version 0.1.11
-------------
*Natural History Museum internal release*
- Fixed #159 - Unable to open jpegs with uppercase filename extension (@quicklizard99)
- Fixed #157 - ingest workflow tool should ignore _thumbnail images (@quicklizard99)
- Fixed #151 - 'Save screen grab' should suggest a filename (@quicklizard99)
- Fixed #150 - Support .bmp (@quicklizard99)
- Fixed #129 - Warn when a read-only document is opened (@quicklizard99)
- Fixed #113 - A shortcut for navigating between the Boxes and Metadata views (@quicklizard99)
- Fixed #94 - Hard-coded keyboard shortcuts in help text (@quicklizard99)
- Fixed #88 - Open-source Data Matrix, 1D barcode, and QR code decoding on all OSes (@quicklizard99)
- Fixed #82 - CMD+backspace on OS X should delete selected boxes (@quicklizard99)

Version 0.1.10
-------------
*Natural History Museum internal release*
- Added #149 - Add metadata templates for Aphididae and Ephemeroptera enhancement (@quicklizard99)
- Fixed #148 - Unable to create new boxes (@quicklizard99)

Version 0.1.9
-------------
*Natural History Museum internal release*
- Work on #88 - Open-source Data Matrix barcode decoding on Linux and Mac OS X (@quicklizard99)
- Work on metadata templates and associated validation (#116) (@quicklizard99)
- Fixed #118 - Rotation arrows on the metadata view do not appear correctly on Windows (@quicklizard99)

Version 0.1.8
-------------
*Natural History Museum internal release*
- Work on #88 - Open-source Data Matrix barcode decoding on Linux and Mac OS X (@quicklizard99)
- Work on #116 - Metadata templates and associated validation (@quicklizard99)
- Fixed #121 - A menu option to save the boxes view to an image file (@quicklizard99)
- Fixed #120 - Show information about the scanned image (@quicklizard99)
- Fixed #117 - Bounding boxes can be created and moved outside of the image (@quicklizard99)

Version 0.1.7
-------------
- Added #138 - Metadata fields to be available on boxes view (@quicklizard99)
- Fixed #137 - Metadata title should not scroll with fields (@quicklizard99)
- Fixed #136 - Reopening the currently open document is confusing (@quicklizard99)
- Added #133 - Show proxy icon on Mac OS X (@quicklizard99)
- Added #132 - Show modified state in title (@quicklizard99)
- Added #109 - Larger images in metadata view (@quicklizard99)

Version 0.1.6
-------------
- Workaround for #130 - Broken barcode reading on Windows (@quicklizard99)
- Work on #116 - Metadata fields are Simple Darwin Core terms (@quicklizard99)
- Work on #84 - Tests (@quicklizard99)
- Fixed #127 - .tif file extension not recognised (@quicklizard99)
- Fixed #125 - Display issue on Windows: After startup, Window title, frame and controls out of screen (@quicklizard99)
- Fixed #124 - "New" doesn't work if inselect document already exists (@quicklizard99)
- Fixed #119 - Non-latin characters in 'Specimen number' metadata field causes grid item title to disappear (@quicklizard99)
- Fixed #115 - Silly wording when a single box selected (@quicklizard99)
- Fixed #106 - Select newly created bounding box (@quicklizard99)
- Fixed #104 - File, Open versus File, New ambiguity (@quicklizard99)
- Fixed #87 - Large images do not display correctly (@quicklizard99)
- Fixed #74 - Mac OS X installer (@quicklizard99)

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
