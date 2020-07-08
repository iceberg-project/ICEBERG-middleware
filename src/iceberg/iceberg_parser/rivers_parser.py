"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""
# pylint: disable=missing-class-docstring, too-few-public-methods


class RiversSubparser():

    def __init__(self, parser):
        rivers_parser = parser.add_parser('rivers')
        rivers_parser.description = 'These are the options for Rivers type \
                                     analysis.'
        rivers_parser.set_defaults(which='rivers')
        rivers_parser.add_argument('--threshold', '-th',
                                   help='Minimum confidence to accept')
        rivers_parser.add_argument('--hyperparameters', '-hy')
        rivers_parser.add_argument('--model', '-m',
                                   help='The size of the scale bands')
        rivers_parser.add_argument('--model_path', '-mp',
                                   help='Path of a custom model')
        rivers_parser.add_argument('--ndwi_path', '-np',
                                   help='Path to Water mask')
