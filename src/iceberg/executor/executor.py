"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""

from __future__ import print_function

import radical.entk as re
import radical.utils as ru

class Executor(object):
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

    def __init__(self, name, resource, queue, walltime, cpus, gpus=0,
                 project=None):

        self._res_dict = {'resource': resource,
                          'walltime': walltime,
                          'cpus': cpus,
                          'gpus': gpus,
                          'schema': 'gsissh',
                          'project': project,
                          'queue':queue}

        self._app_manager = re.AppManager(port=32773,
                                          hostname='localhost',
                                          name=name,
                                          autoterminate=False,
                                          write_workflow=True)

        self._app_manager.resource_dict = self._res_dict

        self._logger = ru.Logger(name='iceberg-middleware', level='INFO')

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

        pass

    def _terminate(self):
        '''
        Stops the execution
        '''

        self._app_manager.resource_terminate()
