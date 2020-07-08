"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""

import argparse
import sys
import json

from .seals_parser import SealsSubparser
from .penguins_parser import PenguinsSubparser
from .rivers_parser import RiversSubparser
from .landcover_parser import LandcoverSubparser

PARSERS = {'seals': SealsSubparser,
           'penguins': PenguinsSubparser,
           'rivers': RiversSubparser,
           'landcover': LandcoverSubparser}


class IcebergParser():
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
            required_args.add_argument('--rmq_username',
                                       help='RMQ user name for EnTK. \
                                             This is RabbitMQ username.',
                                       type=str, default=None)
            required_args.add_argument('--rmq_password',
                                       help='RMQ password. This is the password\
                                       for RMQ.',
                                       type=str, default=None)
            required_args.add_argument('--rmq_endpoint',
                                       help='RMQ endpoint for EnTK. \
                                             This is a url.',
                                       type=str, default=None)
            required_args.add_argument('--rmq_port',
                                       help='RMQ port. This is the port \
                                       number RMQ listens to.',
                                       type=str, default=None)
            required_args.add_argument('--radical_pilot_dburl', '-rpdb',
                                       help='RD MongoDB URL. \
                                       This URL has the following form: \
                                       mongodb://<uname>:<passwd>@ip:port/\
                                           db_name',
                                       type=str, default=None)

            command_parser = parser.add_subparsers(help='commands')

            for key, parser_impl in PARSERS.items():
                parser_impl(command_parser)

            tmp_args = parser.parse_args()
            tmp_args = vars(tmp_args)
        if tmp_args.get('general'):
            self._args = tmp_args
        else:
            self._args['general'] = dict()
            keys = ['cpus',
                    'gpus',
                    'resource',
                    'project',
                    'queue',
                    'walltime',
                    'input_path',
                    'output_path',
                    'rmq_username',
                    'rmq_password',
                    'rmq_endpoint',
                    'rmq_port',
                    'radical_pilot_dburl']
            for key in keys:
                self._args['general'][key] = tmp_args.pop(key)

            self._args['analysis'] = dict()
            self._args['analysis']['which'] = tmp_args.pop('which')
            for key, value in tmp_args.items():
                self._args['analysis'][key] = value

    # --------------------------------------------------------------------------
    #
    def args(self):
        """
        Return a dictionary of the arguments
        """

        return self._args
