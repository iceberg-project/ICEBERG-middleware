"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""

from __future__ import print_function
import argparse
import sys


class IcebergParser(object):
    """
    This class is the argument parser of the ICEBERG software tool.
    """

    def __init__(self):
        """
        The constructor
        """
        parser = argparse.ArgumentParser(description='ICEBERG command description:',
                                         epilog='''Enjoy our tool!''')
        required_args = parser.add_argument_group()
        required_args.title = 'Required Arguments'
        required_args.add_argument('--resource', '-r', help='Where the execution will happen',
                                   type=str)
        required_args.add_argument('--queue', '-q', help='The queue of the resource',
                                   type=str)
        required_args.add_argument('--cpus', '-c', help='How many CPUs will be required',
                                   type=int)
        required_args.add_argument('--gpus', '-g', help='How many GPUs will be required',
                                   type=int)
        required_args.add_argument('--input_path', '-ip', help='Where the input images are',
                                   type=str)
        required_args.add_argument('--output_path', '-op', help='Where the results should be saved',
                                   type=str)
        required_args.add_argument('--walltime', '-w', help='The estimated execution time',
                                   type=int)
        required_args.add_argument('--analysis', '-a', help='The type of analysis to be executed',
                                   type=str)

        if len(sys.argv) < 9:
            parser.print_help()
            if '--help' in sys.argv or '-h' in sys.argv:
                argv = sys.argv.remove('--help')
            elif '-h' in sys.argv:
                argv = sys.argv.remove('-h')
            args = parser.parse_args(argv)
            if args.analysis:
                if args.analysis == '4DGeolocation':
                    usecase = 'four_d_geolocation'
                else:
                    usecase = args.analysis

                if not hasattr(self, usecase):
                    print('Unrecognized Analysis Type')
                else:
                    getattr(self, usecase)(show_help=True)
            exit(1)
        else:
            args = parser.parse_args(sys.argv[1:9])

        if args.analysis == '4DGeolocation':
            usecase = 'four_d_geolocation'
        else:
            usecase = args.analysis

        if not hasattr(self, usecase):
            print('Unrecognized Analysis Type')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        self._usecase_args = None
        getattr(self, usecase)()
        self._args = args

    def seals(self, show_help=False):
        """
        Additional arguments for the Seals Use Case
        """
        seals_args = argparse.ArgumentParser(description='These are the options for Seals type \
                                             analysis.', usage=argparse.SUPPRESS)
        seals_args.add_argument('--scale_bands', '-s', help='The size of the scale bands')
        seals_args.add_argument('--model', '-m', help='The size of the scale bands')
        seals_args.add_argument('--model_path', '-mp', help='Path of a custom model')
        seals_args.add_argument('--hyperparameters', '-hy', help='Hyperparameter Set')

        if show_help:
            seals_args.print_help()
            exit(1)
        elif len(sys.argv[9:]) < 4:
            print('Missing Parameters')
            seals_args.print_help()
            exit(1)

        args = seals_args.parse_args(sys.argv[9:])
        print('Running Seals with ', args)
        self._usecase_args = args

    def penguins(self, show_help=False):
        """
        Additional arguments for the Penguins Use Case
        """
        penguins_args = argparse.ArgumentParser(description='These are the options for Penguins \
                                                type analysis.', usage=argparse.SUPPRESS)
        penguins_args.add_argument('--scale_bands', '-s', help='The size of the scale bands')
        penguins_args.add_argument('--model', '-m', help='The size of the scale bands')
        penguins_args.add_argument('--model_path', '-mp', help='Path of a custom model')
        penguins_args.add_argument('--hyperparameters', '-hy', help='Hyperparameter Set')
        penguins_args.add_argument('--shadow_mask', '-sm')

        if show_help:
            penguins_args.print_help()
            exit(1)
        elif len(sys.argv[9:]) < 5:
            print('Missing Parameters')
            penguins_args.print_help()
            exit(1)

        args = penguins_args.parse_args(sys.argv[9:])
        print('Running Penguins', args)
        self._usecase_args = args

    def four_d_geolocation(self, show_help=False):
        """
        Additional arguments for the 4D Geolocation Use Case
        """
        four_d_geolocation_args = argparse.ArgumentParser(description='These are the options for \
                                                          4DGeolocaltion type analysis.',
                                                          usage=argparse.SUPPRESS)
        four_d_geolocation_args.add_argument('--target_path', '-t', help='Path to target images')
        four_d_geolocation_args.add_argument('--threshold', '-th', help='Minimum, maximum number \
                                                                         of match points')
        four_d_geolocation_args.add_argument('--pixel_accuracy', '-pa', help='An accuracy threshold\
                                                                              for output pixels \
                                                                              when making a match')
        four_d_geolocation_args.add_argument('--source_image_window', '-siw', help='Subset window \
                                                                                    of the source \
                                                                                    image to search \
                                                                                    within')
        four_d_geolocation_args.add_argument('--target_image_window', '-tiw', help='Subset window \
                                                                                    of the target \
                                                                                    image to search \
                                                                                    within')
        four_d_geolocation_args.add_argument('--algorithm', '-a', help='which keypoint search \
                                                                        algorithm to use')

        if show_help:
            four_d_geolocation_args.print_help()
            exit(1)
        elif len(sys.argv[9:]) < 6:
            print('Missing Parameters')
            four_d_geolocation_args.print_help()
            exit(1)

        args = four_d_geolocation_args.parse_args(sys.argv[9:])
        print('Running 4DGeolocation', args)
        self._usecase_args = args

    def rivers(self, show_help=False):
        """
        Additional arguments for the Rivers Use Case
        """
        rivers_args = argparse.ArgumentParser(description='These are the options for Rivers type \
                                              analysis.', usage=argparse.SUPPRESS)
        rivers_args.add_argument('--threshold', '-th', help='Minimum confidence to accept')
        rivers_args.add_argument('--hyperparameters', '-hy')
        rivers_args.add_argument('--model', '-m', help='The size of the scale bands')
        rivers_args.add_argument('--model_path', '-mp', help='Path of a custom model')
        rivers_args.add_argument('--ndwi_path', '-np', help='Path to Water mask')

        if show_help:
            rivers_args.print_help()
            exit(1)
        elif len(sys.argv[9:]) < 5:
            print('Missing Parameters')
            rivers_args.print_help()
            exit(1)

        args = rivers_args.parse_args(sys.argv[9:])
        print('Running Rivers', args)
        self._usecase_args = args

    def landcover(self, show_help=False):
        """
        Additional arguments for the Landcover Use Case
        """
        landcover_args = argparse.ArgumentParser(description='These are the options for Landcover \
                                                 type analysis.', usage=argparse.SUPPRESS)
        landcover_args.add_argument('--spec_lib', '-sl', help='Addition of new ground data to \
                                                               spectral library')
        landcover_args.add_argument('--roi_sel', '-rs', help='Selection of regions of interest for \
                                                              atmospheric correction')
        landcover_args.add_argument('--atmcorr_model', '-am', help='Selection of atmospheric model')
        landcover_args.add_argument('--landcover_lib', '-ll', help='Access landcover masks')
        landcover_args.add_argument('--shadow_mask', '-sm')

        if show_help:
            landcover_args.print_help()
            exit(1)
        elif len(sys.argv[9:]) < 5:
            print('Missing Parameters')
            landcover_args.print_help()
            exit(1)

        args = landcover_args.parse_args(sys.argv[9:])
        print('Running Landcover', args)
        self._usecase_args = args
