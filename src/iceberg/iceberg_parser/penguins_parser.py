"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""

from __future__ import print_function


class PenguinsSubparser(object):

    def __init__(self,parser):
            penguins_parser = parser.add_parser('penguins')            
            penguins_parser.description = 'These are the options for Penguins \
                                           type analysis.'
            penguins_parser.set_defaults(which='penguins')
            penguins_parser.add_argument('--scale_bands', '-s',
                                         help='The size of the scale bands')
            penguins_parser.add_argument('--model', '-m',
                                         help='The size of the scale bands')
            penguins_parser.add_argument('--model_path', '-mp',
                                         help='Path of a custom model')
            penguins_parser.add_argument('--hyperparameters', '-hy',
                                         help='Hyperparameter Set')
            penguins_parser.add_argument('--shadow_mask', '-sm')

