Title: Metadata templates

**Objective**: to configure and use Inselect metadata templates.

This example will cover

* how inselect treats metadata and validation,
* Inselect's metadata template format and
* how to export crops and `CSV` files.

## Preamble

Open `3.Metadata\Scopelodes_spp_Lim_14.inselect`

* This is a SatScan image of pinned insects - moths in family Limacodidae
* Segment the image and refine bounding boxes

![Moths with bounding boxes]({filename}/images/exercises/moths_refined.jpg)

## Metadata template in Inselect

You have complete control over metadata fields and validation through
`.inselect_template` files, which are simple text files that you can edit
using any good text editor.

* Load the `Templates/limacodidae.inselect_template` template by clicking on the
'Simple Darwin Core' button and clicking `Choose...`
* Pink shading over the bounding boxes indicates one or more validation problems,
so we can see at a glance any boxes that need our attention
* The template specifies that the `Location` and `Taxonomy` fields are both
mandatory - newly created bounding boxes have no metadata, so all of the
bounding boxes are shaded pink

![Moths with metadata validation failures]({filename}/images/exercises/moths_template1.jpg)

Click on any of the bounding boxes. The `Location` and `Taxonomy` fields are
both coloured pink.

![Moths with single box selected]({filename}/images/exercises/moths_template2.jpg)

* Set `Location` to Drawer 1
* Set `Taxonomy` to *Scopelodes*
* The pink shading is removed from the fields and box

![Moths with single box selected]({filename}/images/exercises/moths_template3.jpg)

Let's set the metadata for all boxes

* `CTRL + A` to select all boxes
* The field both contain a '\*' to indicate multiple values among boxes
* Set `Location` to Drawer 1 and `Location` to *Scopelodes*

![Moths with all boxes valid]({filename}/images/exercises/moths_template4.jpg)

## Metadata panel

The metadata panel on the right shows
[Simple Darwin Core](http://rs.tdwg.org/dwc/terms/simple/) fields along with
links to definitions.

## Creating and editing metadata templates

Files are in a format called YAML
([YAML Ain't a Markup Language](http://yaml.org/)) - a structured text format.
A reference and examples template files are at
[https://github.com/NaturalHistoryMuseum/inselect-templates](https://github.com/NaturalHistoryMuseum/inselect-templates) -
open this page in a new browser tab and have a quick look through it.

Open `limacodidae.inselect_template` in your text editor:

```
Name: Limacodidae
Object label: '{Taxonomy}-{Location}-{ItemNumber}'
Fields:
    - Name: Taxonomy
      Mandatory: true
      Choices:
          - Anaxidia
          - Anepopsia
          - Apodecta
          - Birthamoides
          - Calcarifera
          - Chalcocelis
          - Comana
          - Comanula
          - Doratifera
          - Ecnomoctena
          - Elassoptila
          - Eloasa
          - Hedraea
          - Hydroclada
          - Lamprolepida
          - Limacochara
          - Mambara
          - Mecytha
          - Parasoidea
          - Praesusica
          - Pseudanapaea
          - Pygmaeomorpha
          - Scopelodes
          - Squamosa
          - Thosea
    - Name: Location
      Mandatory: true
      Choices:
          - Drawer 1
          - Drawer 2
          - Drawer 3
          - Drawer 4
```

When you come to create your own `.inselect_template` files, it is best to
modify an existing template to suit your needs.

## Editing the template

You will append a new, optional free-text field - `Notes` - to the template.

* Use your text editor to add the field to the template
* Click on the 'Limacoididae' button in Inselect and select 'Reload'

## Export metadata and bounding boxes to a CSV file

Click 'Export CSV' in the toolbar and open the `CSV` file in Excel, 
OpenOffice or similar.

Columns are

* `Cropped_image_name` - the filename of the crop
* `ItemNumber` - the number of the bounding box
* Locations of the bounding boxes in
    * normalised (i.e., between 0 and 1) coordinates - `NormalisedLeft`,
      `NormalisedTop`, `NormalisedRight`, `NormalisedBottom`
    * coordinates of the thumbnail image - `ThumbnailLeft`, `ThumbnailTop`,
      `ThumbnailRight`, `ThumbnailBottom`
    * coordinates of the original full-resolution image - `OriginalLeft`,
      `OriginalTop`, `OriginalRight`, `OriginalBottom`

* A column for each of the metadata fields defined in the template
    * `Taxonomy`
    * `Location`
    * `Notes`
