This is an overview of major changes. Refer to the git repository for a full log change.

Version 0.1.15
-------------
- Added #167 - Richer information in about box (@quicklizard)
- Added #126 - Recent documents (@quicklizard)
- Fixed #168 - Information panel shows incorrect file sizes (@quicklizard)
- Fixed #166 - Enter does not toggle Objects view between 'grid' and 'expanded' on Mac OS X (@quicklizard)
- Fixed #134 - Delete box should not scroll Metadata view (@quicklizard)

Version 0.1.14
-------------
- Added #165 - User templates to support thumbnail width pixels (@quicklizard)

Version 0.1.13
-------------
- Work on #156 - User-defined project templates (@quicklizard)
- Fixed #164 - Cropped images not saved with rotation (@quicklizard)
- Fixed #159 - Unable to open jpegs with uppercase filename extension (@quicklizard)
- Fixed #157 - ingest workflow tool should ignore _thumbnail images (@quicklizard)
- Fixed #151 - 'Save screen grab' should suggest a filename (@quicklizard)
- Fixed #150 - Support .bmp (@quicklizard)
- Fixed #129 - Warn when a read-only document is opened (@quicklizard)
- Fixed #121 - A menu option to save the boxes view to an image file (@quicklizard)
- Fixed #120 - Show information about the scanned image (@quicklizard)
- Fixed #117 - Bounding boxes can be created and moved outside of the image (@quicklizard)
- Fixed #113 - A shortcut for navigating between the Boxes and Metadata views (@quicklizard)
- Fixed #94 - Hard-coded keyboard shortcuts in help text (@quicklizard)
- Fixed #88 - Open-source Data Matrix, 1D barcode, and QR code decoding on all OSes (@quicklizard)
- Fixed #82 - CMD+backspace on OS X should delete selected boxes (@quicklizard)

Version 0.1.12
-------------
*Natural History Museum internal release*
- Fixed #161 - Free text metadata template (@quicklizard)
- Fixed #160 - Missing Macrosiphum locations (@quicklizard)

Version 0.1.11
-------------
*Natural History Museum internal release*
- Fixed #159 - Unable to open jpegs with uppercase filename extension (@quicklizard)
- Fixed #157 - ingest workflow tool should ignore _thumbnail images (@quicklizard)
- Fixed #151 - 'Save screen grab' should suggest a filename (@quicklizard)
- Fixed #150 - Support .bmp (@quicklizard)
- Fixed #129 - Warn when a read-only document is opened (@quicklizard)
- Fixed #113 - A shortcut for navigating between the Boxes and Metadata views (@quicklizard)
- Fixed #94 - Hard-coded keyboard shortcuts in help text (@quicklizard)
- Fixed #88 - Open-source Data Matrix, 1D barcode, and QR code decoding on all OSes (@quicklizard)
- Fixed #82 - CMD+backspace on OS X should delete selected boxes (@quicklizard)

Version 0.1.10
-------------
*Natural History Museum internal release*
- Added #149 - Add metadata templates for Aphididae and Ephemeroptera enhancement (@quicklizard)
- Fixed #148 - Unable to create new boxes (@quicklizard)

Version 0.1.9
-------------
*Natural History Museum internal release*
- Work on #88 - Open-source Data Matrix barcode decoding on Linux and Mac OS X (@quicklizard)
- Work on metadata templates and associated validation (#116) (@quicklizard)
- Fixed #118 - Rotation arrows on the metadata view do not appear correctly on Windows (@quicklizard)

Version 0.1.8
-------------
*Natural History Museum internal release*
- Work on #88 - Open-source Data Matrix barcode decoding on Linux and Mac OS X (@quicklizard)
- Work on #116 - Metadata templates and associated validation (@quicklizard)
- Fixed #121 - A menu option to save the boxes view to an image file (@quicklizard)
- Fixed #120 - Show information about the scanned image (@quicklizard)
- Fixed #117 - Bounding boxes can be created and moved outside of the image (@quicklizard)

Version 0.1.7
-------------
- Added #138 - Metadata fields to be available on boxes view (@quicklizard)
- Fixed #137 - Metadata title should not scroll with fields (@quicklizard)
- Fixed #136 - Reopening the currently open document is confusing (@quicklizard)
- Added #133 - Show proxy icon on Mac OS X (@quicklizard)
- Added #132 - Show modified state in title (@quicklizard)
- Added #109 - Larger images in metadata view (@quicklizard)

Version 0.1.6
-------------
- Workaround for #130 - Broken barcode reading on Windows (@quicklizard)
- Work on #116 - Metadata fields are Simple Darwin Core terms (@quicklizard)
- Work on #84 - Tests (@quicklizard)
- Fixed #127 - .tif file extension not recognised (@quicklizard)
- Fixed #125 - Display issue on Windows: After startup, Window title, frame and controls out of screen (@quicklizard)
- Fixed #124 - "New" doesn't work if inselect document already exists (@quicklizard)
- Fixed #119 - Non-latin characters in 'Specimen number' metadata field causes grid item title to disappear (@quicklizard)
- Fixed #115 - Silly wording when a single box selected (@quicklizard)
- Fixed #106 - Select newly created bounding box (@quicklizard)
- Fixed #104 - File, Open versus File, New ambiguity (@quicklizard)
- Fixed #87 - Large images do not display correctly (@quicklizard)
- Fixed #74 - Mac OS X installer (@quicklizard)

Version 0.1.5
-------------
- Icons for plugins (@quicklizard)
- CSV export (@quicklizard)
- Progress box during 'New document' (@quicklizard)
- Open files via drag-drop (@quicklizard)

Version 0.1.4
-------------
- Document format (@quicklizard)
- Workflow tools (@quicklizard)
- UI reimplementation (@quicklizard)
- OS X (Mac) build (@quicklizard)
- Myriad bug fixes and enhancements (@quicklizard)
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
