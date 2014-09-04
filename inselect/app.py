"""Inselect.

Usage:
    main.py
    main.py <filename>
    main.py --batch=input_dir [--recursive --output_dir=<output_dir>]

Options:
  -h --help             Show this screen.
  --version             Show version.
  --batch=<dir>         Input directory
  --recursive           Traverse directory structure recursively.
  --output_dir=<dir>    Output directory of CSV file results. Defaults
                        to the batch input directory.
"""
from __future__ import print_function, division

from PySide import QtGui

import os
import sys
import csv

from .image_viewer import ImageViewer
from .segment import segment_edges
from . import docopt

from skimage import io


def is_image_file(file_name):
    name, ext = os.path.splitext(file_name.lower())
    return ext in [".jpg", ".tiff", ".png"]


def normalized_rects(rects, (height, width)):
    for (x0, y0, x1, y1) in rects:
        yield x0 / width, y0 / height, x1 / width, y1 / height


def save_rects(filename, rects):
    print("Writing CSV file", filename)
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')
        for rect in rects:
            writer.writerow(rect)


def launch_gui(filename=None):
    app = QtGui.QApplication(sys.argv)
    window = ImageViewer(app)
    if filename:
        window.open(filename)
    window.showMaximized()
    window.splitter.setSizes([800, 100])
    window.show()
    sys.exit(app.exec_())


def launch_batch(input_dir=None, output_dir=None, recursive=None):
    """
    Launch batch processor.

    Parameters
    ----------
    input_dir : str
        Default input directory.
    output_dir : str
        Default output directory.  Default is the current directory.
    recursive : bool
        Whether to search the input directory recursively.  Default
        is True.

    """
    if output_dir is None:
        output_dir = "."
    if input_dir is None:
        intput_dir = "."
    if recursive is None:
        recursive = True

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(input_dir):
        print("Batch processing folder: '%s'" % root)

        for filename in files:
            if is_image_file(filename):
                filename = os.path.join(root, filename)
                image = io.imread(filename, plugin='matplotlib')
                height, width, _ = image.shape

                print("Segmenting", filename, image.shape)
                rects = segment_edges(image,
                                      variance_threshold=100,
                                      size_filter=1)

                rects = normalized_rects(rects, (height, width))
                save_rects(filename + '.csv', rects)

        if not recursive:
            break


def launch():
    arguments = docopt(__doc__, version='Inselect 0.1')
    if not arguments["--batch"]:
        print("Launching gui")
        filename = arguments['<filename>']
        launch_gui(filename)
    else:
        print("Batch processing enabled")
        launch_batch(output_dir=arguments["--output_dir"],
                     input_dir=arguments["--batch"],
                     recursive=arguments["--recursive"])
