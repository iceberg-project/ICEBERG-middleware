"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""

class SealsSubparser(object):

    def __init__(self,parser):
            seals_parser = parser.add_parser('seals')
            seals_parser.description = 'These are the options for Seals type \
                                       analysis.'
            seals_parser.set_defaults(which='seals')
            seals_parser.add_argument('--scale_bands', '-s',
                                      help='The size of the scale bands')
            seals_parser.add_argument('--model', '-m',
                                      help='The size of the scale bands')
            seals_parser.add_argument('--model_path', '-mp',
                                      help='Path of a custom model')
            seals_parser.add_argument('--model_arch', '-ma',
                                      help='Model Architecture')
            seals_parser.add_argument('--hyperparameters', '-hy',
                                      help='Hyperparameter Set')
            seals_parser.add_argument('--ve_seals',
                                      help='Path of a python virtualenv with \
                                      the seals package installed ')

