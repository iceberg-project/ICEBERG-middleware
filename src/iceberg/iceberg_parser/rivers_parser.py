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
        rivers_parser.add_argument('-t', '--tile_size', type=int, default=224,
                            help='Tile size')
        rivers_parser.add_argument('-s', '--step', type=int, default=112,
                            help='Step size')
        rivers_parser.add_argument('-w', '--weights_path', type=str,
                            help='Path to the weights')
