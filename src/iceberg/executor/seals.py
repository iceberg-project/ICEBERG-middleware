"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""

from __future__ import print_function
import os

from .executor import Executor
from ..discovery import Discovery


class Seals(Executor):
    '''
    :Class Seals:
    This class instantiates the Seals use case.
    :Additional Parameters:
        :input_path: The path to the input images
        :ouptut_path: Path to the output images
        :scale_bands: The size of the scale bands
        :model: The model
        :model_path: Path of a custom model
        :hyperparameters: Hyperparameter Set
    '''

    def __init__(self, name, resources, project=None, input_path=None,
                 output_path=None, scale_bands=None, model=None,
                 model_path=None, hyperparameters=None):

        super(Seals, self).__init__(name=name,
                                    resource=resources['resource'],
                                    queue=resources['queue'],
                                    walltime=resources['walltime'],
                                    cpus=resources['cpus'],
                                    gpus=resources['gpus'],
                                    project=project)
        self._data_input_path = input_path
        self._output_path = output_path
        self._scale_bands = scale_bands
        self._model_name = model
        self._model_path = model_path
        self._hyperparam = hyperparameters
        self._req_modules = None
        self._pre_execs = None

        if self._res_dict['resource'] == 'xsede.bridges':

            self._req_modules = ['psc_path/1.1', 'slurm/default', 'intel/17.4',
                                 'python3', 'cuda']

            self._pre_execs = ['source $SCRATCH/pytorchCuda/bin/activate',
                               'export PYTHONPATH=$SCRATCH/pytorchCuda/lib/'
                               + 'python3.5/site-packages:$PYTHONPATH']

        self._logger.info('Seals initialized')

    def run(self):
        '''
        This is a blocking execution method. This method should be called to
        execute the usecase.
        '''
        try:
            self._logger.debug('Running workflow')
            self._run_workflow()
        finally:
            self._terminate()

    def _run_workflow(self):
        '''
        Private method that creates and executes the workflow of the use case.
        '''
        self._app_manager.shared_data = [os.path.abspath(self._model_path
                                                         + self._model_name)]
        self._logger.debug('Uploaded model %s',
                           os.path.abspath(self._model_path + self._model_name))
        discovery = Discovery(modules=self._req_modules,
                              paths=self._data_input_path,
                              pre_execs=self._pre_execs)
        discovery_pipeline = discovery.generate_discover_pipeline()

        self._app_manager.workflow = set([discovery_pipeline])

        self._app_manager.run()

    def _terminate(self):
        '''
        Stops the execution
        '''

        self._app_manager.resource_terminate()
