"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""

from __future__ import print_function
import argparse
import sys
import json


class IcebergParser(object):
    """
    This class is the argument parser of the ICEBERG software tool.
    """
    # --------------------------------------------------------------------------
    #
    def __init__(self):
        """
        The constructor
        """

        self._args = dict()
        if '--config' in sys.argv:
            parser = argparse.ArgumentParser()

            parser.add_argument('--config', help='JSON config file',
                                type=str, required=True)

            cfg_arg = parser.parse_args()
            with open(cfg_arg.config) as cfg:
                tmp_args = json.load(cfg)
        else:
            parser = argparse.ArgumentParser(description='ICEBERG command \
                                             description:',
                                             epilog='''Enjoy our tool!''')

            required_args = parser.add_argument_group()
            required_args.title = 'Required Arguments'
            required_args.add_argument('--resource', '-r',
                                       help='Where the execution will happen',
                                       type=str, required=True)
            required_args.add_argument('--queue', '-q',
                                       help='The queue of the resource',
                                       type=str, default=None)
            required_args.add_argument('--cpus', '-c',
                                       help='How many CPUs will be required',
                                       type=int, required=True)
            required_args.add_argument('--gpus', '-g',
                                       help='How many GPUs will be required',
                                       type=int, required=True)
            required_args.add_argument('--input_path', '-ip',
                                       help='Where the input images are',
                                       type=str, required=True)
            required_args.add_argument('--output_path', '-op',
                                       help='Where the results should be saved',
                                       type=str, required=True)
            required_args.add_argument('--walltime', '-w',
                                       help='The estimated execution time',
                                       type=int, required=True)
            required_args.add_argument('--project', '-pr',
                                       help='The project ID to charge',
                                       type=str, default=None)

            command_args = parser.add_subparsers(help='commands')
            seals_parser = command_args.add_parser('seals')
            penguins_parser = command_args.add_parser('penguins')
            four_d_geoloc_parser = command_args.add_parser('4Dgeolocation')
            rivers_parser = command_args.add_parser('rivers')
            landcover_parser = command_args.add_parser('landcover')

            seals_parser.description = 'These are the options for Seals type \
                                       analysis.'
            seals_parser.set_defaults(which='seals')
            seals_parser.add_argument('--scale_bands', '-s',
                                      help='The size of the scale bands')
            seals_parser.add_argument('--model', '-m',
                                      help='The size of the scale bands')
            seals_parser.add_argument('--model_path', '-mp',
                                      help='Path of a custom model')
            seals_parser.add_argument('--hyperparameters', '-hy',
                                      help='Hyperparameter Set')

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

            four_d_geoloc_parser.description = 'These are the options for \
                                                4DGeolocaltion type analysis.'
            four_d_geoloc_parser.set_defaults(which='4DGeolocation')
            four_d_geoloc_parser.add_argument('--target_path', '-t',
                                              help='Path to target images')
            four_d_geoloc_parser.add_argument('--threshold', '-th',
                                              help='Minimum, maximum number of \
                                              match points')
            four_d_geoloc_parser.add_argument('--pixel_accuracy', '-pa',
                                              help='An accuracy threshold for \
                                              output pixels when making a \
                                              match')
            four_d_geoloc_parser.add_argument('--source_image_window', '-siw',
                                              help='Subset window of the \
                                              source image to search within')
            four_d_geoloc_parser.add_argument('--target_image_window', '-tiw',
                                              help='Subset window of the \
                                              target image to search within')
            four_d_geoloc_parser.add_argument('--algorithm', '-a',
                                              help='which keypoint search \
                                              algorithm to use')

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

            tmp_args = parser.parse_args()
            tmp_args = vars(tmp_args)
        if tmp_args.get('general'):
            self._args = tmp_args
        else:
            self._args['general'] = dict()
            self._args['general']['cpus'] = tmp_args.pop('cpus')
            self._args['general']['gpus'] = tmp_args.pop('gpus')
            self._args['general']['resource'] = tmp_args.pop('resource')
            self._args['general']['project'] = tmp_args.pop('project')
            self._args['general']['queue'] = tmp_args.pop('queue')
            self._args['general']['waltime'] = tmp_args.pop('walltime')
            self._args['general']['input_path'] = tmp_args.pop('input_path')
            self._args['general']['output_path'] = tmp_args.pop('output_path')

            self._args['analysis'] = dict()
            self._args['analysis']['which'] = tmp_args.pop('which')
            for key, value in tmp_args.iteritems():
                self._args['analysis'][key] = value

    # --------------------------------------------------------------------------
    #
    def args(self):
        """
        Return a dictionary of the arguments
        """

        return self._args
