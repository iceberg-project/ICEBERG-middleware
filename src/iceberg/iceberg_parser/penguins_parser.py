"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""
# pylint: disable=missing-class-docstring, too-few-public-methods


class PenguinsSubparser():

    def __init__(self, parser):
        penguins_parser = parser.add_parser('penguins')
        penguins_parser.description = 'These are the options for Penguins \
                                       type analysis.'
        penguins_parser.set_defaults(which='penguins')
        penguins_parser.add_argument('--epoch', '-ep',
                                     help='The number of epoches default is \
                                     set to 300')
        penguins_parser.add_argument('--model', '-m',
                                     help='The model name')
        penguins_parser.add_argument('--model_path', '-mp',
                                     help='Path of a custom model')
        penguins_parser.add_argument('--ve_penguins')
