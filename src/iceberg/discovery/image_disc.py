"""
Image Discovery Kernel
==========================================================
This script takes as input a path and returns a dataframe
with all the images and their size.
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""
from glob import glob
import argparse
import os
import math
import csv


def image_discovery(path, filename='list', filetype='csv', filesize=False,
                    image_ftype='tif'):
    """
    This function creates a dataframe with image names and size from a path.
    :Arguments:
        :path: Images path, str
        :filename: The filename of the CSV file containing the dataframe.
                   Default Value: list.csv
        :filesize: Whether or not the image sizes should be inluded to the
                   dataframe. Default value: False
    """

    filepaths = glob(path + '/*.%s' % image_ftype)
    image_csv = open(filename + '.' + filetype, 'wt')
    writer = csv.writer(image_csv)
    if filesize:
        writer.writerow(('Filename', 'Size'))
        for filepath in filepaths:
            filesize = int(math.ceil(os.path.getsize(filepath) / 1024 / 1024))
            writer.writerow((filepath, filesize))
    else:
        writer.writerow(['Filename'])
        for filepath in filepaths:
            writer.writerow([filepath])

    image_csv.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to a remote resource where data \
                        are')
    parser.add_argument('--image_ftype', type=str, help='The filetype of \
                         the images')
    parser.add_argument('--filename', type=str, default='list',
                        help='Name of the output file')
    parser.add_argument('--filetype', type=str, default='csv',
                        help='Type of the output file')
    parser.add_argument('--filesize', help='Include the filesize to the \
                        output CSV', action='store_true')
    args = parser.parse_args()

    image_discovery(args.path, args.filename, args.filetype, args.filesize,
                    args.image_ftype)
