#!/usr/bin/env python
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
from PySide import QtGui

import cv2
import os
import sys
import csv

from inselect.image_viewer import ImageViewer
from inselect.segment import segment_edges
from inselect import docopt


def is_image_file(file_name):
    name, ext = os.path.splitext(file_name.lower())
    return ext in [".jpg", ".tiff", ".png"]


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Inselect 0.1')
    if not arguments["--batch"]:
        print "Launching gui."
        app = QtGui.QApplication(sys.argv)
        window = ImageViewer(app)
        if arguments['<filename>']:
            window.open(arguments['<filename>'])
        window.showMaximized()
        window.show()
        sys.exit(app.exec_())
    else:
        print "Batch processing mode"
        output_dir = ""
        if arguments["--output_dir"]:
            output_dir = arguments["--output_dir"]
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        else:
            output_dir = os.path.dirname(filename)
        for root, dirs, files in os.walk(arguments["--batch"]):
            print "Processing", root
            for file_name in files:
                if is_image_file(file_name):
                    file_name = os.path.join(root, file_name)
                    image = cv2.imread(file_name)
                    height, width, _ = image.shape
                    print "Segmenting", file_name, image.shape
                    rects = segment_edges(image,
                                          variance_threshold=100,
                                          size_filter=1)
                    csv_file_name = file_name + '.csv'
                    print "Writing csv file", csv_file_name
                    with open(csv_file_name, 'w') as csvfile:
                        writer = csv.writer(csvfile, delimiter=' ')
                        for box in rects:
                            box = [float(value) for value in box]
                            box[0] /= width
                            box[1] /= height
                            box[2] /= width
                            box[3] /= height
                            writer.writerow(box)
            if not arguments["--recursive"]:
                break
