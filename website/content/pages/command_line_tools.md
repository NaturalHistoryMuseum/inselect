Title: Command-line tools

* If you expect to be working on batches of hundreds or thousands of images
* An advanced topic

If you have never worked with the Windows command line or the Mac terminal then
we recommend that you get training from your IT staff or someone who has
relevant experience.

**Objective**: to ingest the five example image files in `6.CommandLineTools` and
apply the cookie cutter that you previously created.

This example will provide an introduction to Inselect's command line tools.

## Workflow

![Inselect workflow]({filename}/images/exercises/workflow.svg)

Each of the operations shown in blue has an associated command-line tool.
You can pick and choose the relevant command-line tools together with cookie
cutters and metadata templates to integrate Inselect into your existing
workflows.
Descriptions of each tool are below.

### `ingest`
* You provide the paths to an input directory and on output directory; these can
be the same
* For each image file in the input directory
    * Moves the image to the output directory
    * Creates the `.inselect` file
    * Create the thumbnail `JPG`; you can provide the resolution
    * Optionally applies a cookie cutter

### `segment`
* You provide the path to a directory
* For each `.inselect` file in the directory
    * Runs automatic segmentation
    * You can specify whether to sort boxes by columns or by rows
    * Ignores `.inselect` files that already have bounding boxes

### `read_barcodes`
* You provide the path to a directory
* For each `.inselect` file in the directory
    * Reads barcodes using the reader that you specify

### `export_metadata`
* You provide the path to a directory
* For each `.inselect` file in the directory
    * Writes a `CSV` file of metadata
    * You can specify an Inselect template file
    * Files with validations errors are ignored

### `save_crops`
* You provide the path to a directory
* For each `.inselect` file in the directory
    * Writes cropped images
    * You specify an optional Inselect template file that will be used to format the
    crop filenames
    * Files with validations errors are ignored

## Test that you can run tools

Start the Windows command prompt.
The following code fragments assume that you installed Inselect to the default
location of `C:\Program Files\inselect`. You should alter the paths as required,
if you installed the program to a different directory.

Each tool supports the `--help` argument:

```
C:\Program Files\inselect\ingest.exe --help
```

You should see
```
usage: ingest.exe [-h] [-c COOKIE_CUTTER] [-w THUMBNAIL_WIDTH] [--debug] [-v]
                  inbox docs

Ingests images into Inselect

positional arguments:
  inbox                 Source directory containing scanned images
  docs                  Destination directory to which images will be moved
                        and in which Inselect documents will be created. Can
                        be the same as inbox.

optional arguments:
  -h, --help            show this help message and exit
  -c COOKIE_CUTTER, --cookie-cutter COOKIE_CUTTER
                        Path to a '.inselect_cookie_cutter' file that will be
                        applied to new Inselect documents
  -w THUMBNAIL_WIDTH, --thumbnail-width THUMBNAIL_WIDTH
                        The width of the thumbnail in pixels; defaults to 4096
  --debug
  -v, --version         show program's version number and exit
```

## Ingest images

The `6.CommandLineTools` directory contains five `JPG` files. Run

```
C:\Program Files\inselect\ingest.exe --thumbnail-width 8000 \
    --cookie-cutter <path to the inselect_cookie_cutter file> \
    <path to the 6.CommandLineTools directory> \
    <path to the 6.CommandLineTools directory>
```

* What did the `ingest` tool report?
* One of the image files has a deliberate error - how did the `ingest` tool
behave?
