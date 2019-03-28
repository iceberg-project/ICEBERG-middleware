"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""

from __future__ import print_function
import argparse
import sys

class IcebergParser(object):

    def __init__(self):
        parser = argparse.ArgumentParser(description='ICEBERG command description:',
                                         usage='''iceberg <resource> <queue> 
                                                  <cpus> <gpus> <input path> 
                                                  <output path> <wall time> 
                                                  <use case> [<args>]''',
                                         epilog='''Have fun! :)''')
        parser.add_argument('--resource', help='Where the execution will happen', required=True)
        parser.add_argument('--queue', help='The queue of the resource', required=True)
        parser.add_argument('--cpus', help='How many CPUs will be required', required=True)
        parser.add_argument('--gpus', help='How many GPUs will be required', required=True)
        parser.add_argument('--input_path', help='Where the input images are', required=True)
        parser.add_argument('--output_path', help='Where the results should be saved', required=True)
        parser.add_argument('--walltime', help='The estimated execution time', required=True)
        parser.add_argument('--analysis', help='The type of analysis to be executed', required=True)
        parser._optionals.title = 'Required arguments'
    
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        if len(sys.argv) < 9:
            parser.print_help()
            exit(1)

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
        use_case_args = getattr(self, usecase)()
        self._args = args
        self._usecase_args = use_case_args


    def seals(self):
        seals_args = argparse.ArgumentParser(description='These are the options for Seals type analysis.')
        seals_args.add_argument('--scale_bands', '-s', help='The size of the scale bands')
        seals_args.add_argument('--model', '-m', help='The size of the scale bands')
        seals_args.add_argument('--model_path', '-mp', help='Path of a custom model')
        seals_args.add_argument('--hyperparameters', '-hy', help='Hyperparameter Set')
        
        if len(sys.argv[9:]) < 4:
            print('Missing Parameters')
            seals_args.print_help()
            exit(1)

        args = seals_args.parse_args(sys.argv[9:])
        print('Running Seals with ', args)
        return args

    def penguins(self):
        penguins_args = argparse.ArgumentParser(description='These are the options for Penguins type analysis.')
        penguins_args.add_argument('--scale_bands', '-s', help='The size of the scale bands')
        penguins_args.add_argument('--model', '-m', help='The size of the scale bands')
        penguins_args.add_argument('--model_path', '-mp', help='Path of a custom model')
        penguins_args.add_argument('--hyperparameters', '-hy', help='Hyperparameter Set')
        penguins_args.add_argument('--shadow_mask', '-sm')
        
        if len(sys.argv[9:]) < 5:
            print('Missing Parameters')
            penguins_args.print_help()
            exit(1)

        args = penguins_args.parse_args(sys.argv[9:])
        print('Running Penguins', args)
        return args

    def four_d_geolocation(self):
        four_d_geolocation_args = argparse.ArgumentParser(description='These are the options for 4DGeolocaltion type analysis.')
        four_d_geolocation_args.add_argument('--target_path', '-t', help='Path to target images')
        four_d_geolocation_args.add_argument('--threshold', '-th', help='Minimum, maximum number of match points')
        four_d_geolocation_args.add_argument('--pixel_accuracy', '-pa', help='An accuracy threshold for output pixels when making a match')
        four_d_geolocation_args.add_argument('--source_image_window', '-siw', help='Subset window of the source image to search within')
        four_d_geolocation_args.add_argument('--target_image_window', '-tiw', help='Subset window of the target image to search within')
        four_d_geolocation_args.add_argument('--algorithm', '-a', help='which keypoint search algorithm to use')
        
        if len(sys.argv[9:]) < 6:
            print('Missing Parameters')
            four_d_geolocation_args.print_help()
            exit(1)

        args = four_d_geolocation_args.parse_args(sys.argv[9:])
        print('Running 4DGeolocation', args)
        return args

    def rivers(self):
        rivers_args = argparse.ArgumentParser(description='These are the options for Rivers type analysis.')
        rivers_args.add_argument('--threshold', '-th', help='Minimum confidence to accept')
        rivers_args.add_argument('--hyperparameters', '-hy')
        rivers_args.add_argument('--model', '-m', help='The size of the scale bands')
        rivers_args.add_argument('--model_path', '-mp', help='Path of a custom model')
        rivers_args.add_argument('--ndwi_path', '-np', help='Path to Water mask')
        
        if len(sys.argv[9:]) < 5:
            print('Missing Parameters')
            rivers_args.print_help()
            exit(1)

        args = rivers_args.parse_args(sys.argv[9:])
        print('Running Rivers', args)
        return args

    def landcover(self):
        landcover_args = argparse.ArgumentParser(description='These are the options for Landcover type analysis.')
        landcover_args.add_argument('--spec_lib', '-sl', help='Addition of new ground data to spectral library')
        landcover_args.add_argument('--roi_sel', '-rs', help='Selection of regions of interest for atmospheric correction')
        landcover_args.add_argument('--atmcorr_model', '-am', help='Selection of atmospheric model')
        landcover_args.add_argument('--landcover_lib', '-ll', help='Access landcover masks')
        landcover_args.add_argument('--shadow_mask', '-sm')
        
        if len(sys.argv[9:]) < 5:
            print('Missing Parameters')
            landcover_args.print_help()
            exit(1)

        args = landcover_args.parse_args(sys.argv[9:])
        print('Running Landcover', args)
        return args

if __name__ == '__main__':
    IcebergParser()
