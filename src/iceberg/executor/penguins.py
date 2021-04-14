"""
Author: Aymen Alsaadi
License: MIT
Copyright: 2019-2020
"""

from __future__ import print_function
import os
import csv
import radical.entk as re

from .executor import Executor
from ..discovery import Discovery


class Penguins(Executor):
    '''
    :Class Penguins:
    This class instantiates the Penguins use case.
    :Additional Parameters:
    :input_path: The path to the input images
        :ouptut_path: Path to the output images
        :model: The model name
        :model_path: Path of a custom model
        :epoch: number of epochs (300)
    '''
    # pylint: disable=too-many-arguments
    def __init__(self, name, resources, project=None, input_path=None,
                 output_path=None, gpu_ids=None, model=None,
                 model_path=None, epoch=None):
        print(resources)
        super(Penguins, self).__init__(name=name,
                                       resource=resources['resource'],
                                       queue=resources['queue'],
                                       walltime=resources['walltime'],
                                       cpus=resources['cpus'],
                                       gpus=resources['gpus'],
                                       project=project)
        self._gpu_ids = gpu_ids
        self._data_input_path = input_path
        self._output_path = output_path
        self._model_name = model
        self._model_path = model_path
        self._epoch = epoch
        self._req_modules = None
        self._pre_execs = None
        self._env_var = os.environ.get('VE_PENGUINS')
        if self._res_dict['resource'] == 'xsede.bridges':

            self._req_modules = ['cuda', 'python3']

            self._pre_execs = ['source %s' % self._env_var
                               + '/bin/activate',
                               'export PYTHONPATH=%s/' % self._env_var
                               + 'lib/python3.5/site-packages']

        self._logger.info('Penguins initialized')

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

    def _resolve_pre_execs(self):
        '''
        This is a utils method. It takes the list of modules and return a list
        of pre_exec commands
        '''

        tmp_pre_execs = list()
        for module in self._req_modules:
            tmp_pre_exec = 'module load %s' % module
            self._logger.debug("Preexec added: %s", tmp_pre_exec)
            tmp_pre_execs.append(tmp_pre_exec)

        tmp_pre_execs = tmp_pre_execs + self._pre_execs

        return tmp_pre_execs

    def _generate_pipeline(self, name, pre_execs, image, gpu_id):

        '''
        This function creates a pipeline for an image that will be analyzed.

        :Arguments:
            :name: Pipeline name, str
            :image: image path, str
            :model_path: Path to the model file, str
            :model_arch: Prediction Model Architecture, str
            :model_name: Prediction Model Name, str
            :hyperparam_set: Which hyperparameter set to use, str
        '''
        # Create a Pipeline object
        entk_pipeline = re.Pipeline()
        entk_pipeline.name = name
        # Create a Stage object
        stage0 = re.Stage()
        stage0.name = '%s-S0' % (name)
        # Create Task 1, training
        task1 = re.Task()
        task1.name = '%s-T0' % stage0.name
        task1.pre_exec = pre_execs
        task1.executable = 'iceberg_penguins.detect'  # Assign task executable
        # Assign arguments for the task executable
        task1.arguments = ['--gpu_ids', gpu_id,
                           '--name', self._model_name,
                           '--epoch', self._epoch,
                           '--checkpoints_dir', self._model_path,
                           '--output', self._output_path,
                           '--testset', 'GE',
                           '--input_im', image.split('/')[-1]]
        task1.link_input_data = ['%s' % image]
        task1.cpu_reqs = {'cpu_processes': 1, 'cpu_threads': 1,
                          'cpu_process_type': None, 'cpu_thread_type': 'OpenMP'}
        task1.gpu_reqs = {'gpu_processes': 1, 'gpu_threads': 1,
                          'gpu_process_type': None, 'gpu_thread_type': 'OpenMP'}
        # Download resuting images
        # task1.download_output_data = ['%s/ > %s' % (image.split('/')[-1].
        #                                            split('.')[0],
        #                                            image.split('/')[-1])]
        # task1.tag = task0.name

        stage0.add_tasks(task1)
        # Add Stage to the Pipeline
        entk_pipeline.add_stages(stage0)

        return entk_pipeline

    def _run_workflow(self):
        '''
        Private method that creates and executes the workflow of the use case.
        '''

        discovery = Discovery(modules=self._req_modules,
                              paths=self._data_input_path,
                              pre_execs=self._pre_execs)
        discovery_pipeline = discovery.generate_discover_pipe(img_ftype='png')

        self._app_manager.workflow = set([discovery_pipeline])

        self._app_manager.run()
        images_csv = open('images0.csv')
        images = csv.reader(images_csv)
        _ = next(images)
        pre_execs = self._resolve_pre_execs()
        img_pipelines = list()
        idx = 0
        for [image, _] in images:
            img_pipe = self._generate_pipeline(name='P%s' % idx,
                                               pre_execs=pre_execs,
                                               image=image,
                                               gpu_id=0)
            img_pipelines.append(img_pipe)
            idx += 1
        images_csv.close()
        self._app_manager.workflow = set(img_pipelines)

        self._app_manager.run()

    def _terminate(self):
        '''
        Stops the execution
        '''

        self._app_manager.resource_terminate()
