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
            penguins_parser.set_defaults(which='penguins'),
            penguins_parser.add_argument('--gpu_ids', '-gid',
                                         help='The GPU id 0 or 1'),
            penguins_parser.add_argument('--epoch', 'ep',
                                         help='The number of epoches default is \
                                         set to 300'),
            penguins_parser.add_argument('--model', '-m',
                                         help='The model name'),
            penguins_parser.add_argument('--model_path', '-mp',
                                         help='Path of a custom model')


