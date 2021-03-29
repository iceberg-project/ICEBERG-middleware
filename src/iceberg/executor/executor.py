"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""

import os

import radical.entk as re
import radical.utils as ru


class Executor():
    '''
    :Class Executor:
    This base class is for executing workflows.
    :Parameters:
        :name: name of the execution. It has to be a unique value
        :resource: HPC resource on which the script will run
        :queue: The queue from which resources are requested.
        :walltime: The amount of time resources are requested in minutes
        :cpus: The number of CPUs required for execution
        :gpus: The number of GPUs required for execution
        :project: The project that will be charged
    '''

    def __init__(self, name, resource, walltime, cpus, gpus=0,
                 project=None, queue=None):

        self._res_dict = {'resource': resource,
                          'walltime': walltime,
                          'cpus': cpus,
                          'gpus': gpus}

        if project:
            self._res_dict['project'] = project

        if queue:
            self._res_dict['queue'] = queue

        if 'local.localhost' in resource:
            self._res_dict['access_schema'] = 'ssh'
        else:
            self._res_dict['access_schema'] = 'gsissh'

        rmq_endpoint = os.environ.get('RMQ_ENDPOINT', None)
        rmq_port = os.environ.get('RMQ_PORT', None)
        rmq_username = os.environ.get('RMQ_USERNAME', None)
        rmq_passwd = os.environ.get('RMQ_PASSWORD', None)
        if ((rmq_endpoint is None) or (rmq_port is None)):
            raise RuntimeError('Rabbit MQ endpoint and/or port is not set')

        self._app_manager = re.AppManager(port=int(rmq_port),
                                          hostname=rmq_endpoint,
                                          username=rmq_username,
                                          password=rmq_passwd,
                                          name=name,
                                          autoterminate=False,
                                          write_workflow=False)

        self._app_manager.resource_desc = self._res_dict

        self._logger = ru.Logger(name='iceberg-middleware', level='DEBUG')

    def run(self):
        '''
        This is a blocking execution method. This method should be called to
        execute the usecase.
        '''

        self._run_workflow()

        self._terminate()

    def _run_workflow(self):
        '''
        Private method that creates and executes the workflow of the use case.
        '''

    def _terminate(self):
        '''
        Stops the execution
        '''

        self._app_manager.resource_terminate()
