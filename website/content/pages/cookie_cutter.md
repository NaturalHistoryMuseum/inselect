Title: Cookie cutter

The microscope slides are arranged on a 20 x 5 template. If you are regularly
dealing with hundreds or thousands of scanned images with an identical
arrangement of objects then automatic segmentation is imperfect.

**Objective**: to create and use cookie cutter templates.

This example will cover creating and applying cookie cutter template.

## Create cookie cutter template for slides

* Open `5.CookieCutter/Drawer_76_77_78_79_81_83a.inselect`
* Segment and delete the erroneous boxes
* Check that the 100 bounding boxes are in the right places
* Click 'Cookie cutter' on the toolbar and select 'Save boxes to new cookie cutter...'
and call it `20 x 5 slides`
* Inselect saves the bounding boxes only to the template - metadata is not saved
* Inselect sets the new file as the current cookie cutter

## Apply cookie cutter

* Open `5.CookieCutter/Drawer_60b_61_62a.jpg`
* Inselect creates boxes using cookie cutter
* Select all, zoom in, fine tune exact positons with mouse or keyboard

Cookie cutters have proved to be a time saver but they are an unsatisfactory,
crude solution and we would like a more automated method.
