"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""
# pylint: disable=missing-class-docstring, too-few-public-methods


class SealsSubparser():

    def __init__(self, parser):
        seals_parser = parser.add_parser('seals')
        seals_parser.description = 'These are the options for Seals type \
                                   analysis.'
        seals_parser.set_defaults(which='seals')
        seals_parser.add_argument('--bands', '-b', required=False, type=str, default='0',
                            help='string with bands seperated by commas. defaults to 0 for the panchromatic band')
        seals_parser.add_argument('--stride', '-s', type=float, default=1.0, required=False,
                            help='distance between tiles as a multiple of patch_size. defaults to 1.0, i.e. adjacent '
                                'tiles without overlap')
        seals_parser.add_argument('--patch_size', '-p', type=int, default=224, required=False,
                            help='side dimensions for each patch. patches are required to be squares.')
        seals_parser.add_argument('--geotiff', '-g', type=int, default=0, required=False,
                            help='boolean for whether to keep geographical information.')

        seals_parser.add_argument('--model_architecture', type=str,
                        default='UnetCntWRN', help='model architecture, must be a member of models '
                                                   'dictionary')
        seals_parser.add_argument('--hyperparameter_set', type=str,
                        default='B', help='combination of hyperparameters used, must be a member '
                                          'of hyperparameters dictionary')
        seals_parser.add_argument('--model_name', type=str, default='UnetCntWRN_ts-vanilla',
                        help='name of input model file from training, this name will also be '
                             'used in subsequent steps of the pipeline')
        seals_parser.add_argument('--models_folder', type=str, default='saved_models',
                                  help='folder where the model tar file is saved')
        seals_parser.add_argument('--ve_seals',
                                  help='Path of a python virtualenv with \
                                  the seals package installed ')
