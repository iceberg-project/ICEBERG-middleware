"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""
# pylint: disable=missing-class-docstring, too-few-public-methods


class LandcoverSubparser():

    def __init__(self, parser):
        landcover_parser = parser.add_parser('landcover')
        landcover_parser.description = 'These are the options for \
                                        Landcover type analysis.'
        landcover_parser.set_defaults(which='landcover')
        landcover_parser.add_argument('--spec_lib', '-sl',
                                      help='Addition of new ground data to \
                                      spectral library')
        landcover_parser.add_argument('--roi_sel', '-rs',
                                      help='Selection of regions of \
                                      interest for atmospheric correction')
        landcover_parser.add_argument('--atmcorr_model', '-am',
                                      help='Selection of atmospheric model')
        landcover_parser.add_argument('--landcover_lib', '-ll',
                                      help='Access landcover masks')
        landcover_parser.add_argument('--shadow_mask', '-sm')
