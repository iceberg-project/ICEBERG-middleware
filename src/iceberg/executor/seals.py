"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""

from __future__ import print_function
import os
import csv
import radical.entk as re

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
    # pylint: disable=too-many-arguments
    def __init__(self, name, resources, project=None, input_path=None,
                 output_path=None, scale_bands=None, model=None,
                 model_path=None, model_arch=None, hyperparameters=None):

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
        self._model_arch = model_arch
        self._hyperparam = hyperparameters
        self._req_modules = None
        self._pre_execs = None
        self._env_var = os.environ.get('VE_SEALS')
        if self._res_dict['resource'] == 'xsede.bridges':

            self._req_modules = ['cuda', 'python3']

            self._pre_execs = ['source %s' % self._env_var
                               + '/bin/activate',
                               'export PYTHONPATH=%s/' % self._env_var
                               + 'lib/python3.5/site-packages']

        self._logger.info('Seals initialized')
    # pylint: disable=too-many-arguments

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

    def _generate_pipeline(self, name, pre_execs, image, image_size):

        '''
        This function creates a pipeline for an image that will be analyzed.

        :Arguments:
            :name: Pipeline name, str
            :image: image path, str
            :image_size: image size in MBs, int
            :tile_size: The size of each tile, int
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
        task0 = re.Task()
        task0.name = '%s-T0' % stage0.name
        task0.pre_exec = pre_execs
        task0.executable = 'iceberg_seals.tiling'  # Assign tak executable
        # Assign arguments for the task executable
        task0.arguments = ['--scale_bands=%s' % self._scale_bands,
                           '--input_image=%s' % image.split('/')[-1],
                           # This line points to the local filesystem of the
                           # node that the tiling of the image happened.
                           '--output_folder=$NODE_LFS_PATH/%s' % task0.name]
        task0.link_input_data = [image]
        task0.cpu_reqs = {'processes': 1, 'threads_per_process': 4,
                          'process_type': None, 'thread_type': 'OpenMP'}
        task0.lfs_per_process = image_size

        stage0.add_tasks(task0)
        # Add Stage to the Pipeline
        entk_pipeline.add_stages(stage0)

        # Create a Stage object
        stage1 = re.Stage()
        stage1.name = '%s-S1' % (name)
        # Create Task 1, training
        task1 = re.Task()
        task1.name = '%s-T1' % stage1.name
        task1.pre_exec = pre_execs
        task1.executable = 'iceberg_seals.predicting'  # Assign task executable
        # Assign arguments for the task executable
        task1.arguments = ['--input_image', image.split('/')[-1],
                           '--model_architecture', self._model_arch,
                           '--hyperparameter_set', self._hyperparam,
                           '--training_set', 'test_vanilla',
                           '--test_folder', '$NODE_LFS_PATH/%s' % task0.name,
                           '--model_path', './',
                           '--output_folder', './%s' % image.split('/')[-1].
                           split('.')[0]]
        task1.link_input_data = ['$SHARED/%s' % self._model_name]
        task1.cpu_reqs = {'processes': 1, 'threads_per_process': 1,
                          'process_type': None, 'thread_type': 'OpenMP'}
        task1.gpu_reqs = {'processes': 1, 'threads_per_process': 1,
                          'process_type': None, 'thread_type': 'OpenMP'}
        # Download resuting images
        task1.download_output_data = ['%s/ > %s' % (image.split('/')[-1].
                                                    split('.')[0],
                                                    image.split('/')[-1])]
        task1.tag = task0.name

        stage1.add_tasks(task1)
        # Add Stage to the Pipeline
        entk_pipeline.add_stages(stage1)

        return entk_pipeline

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
                              pre_execs=self._pre_execs + ['module list',
                                                           'echo $PYTHONPATH',
                                                           'which python3'])
        discovery_pipeline = discovery.generate_discover_pipeline()

        self._app_manager.workflow = set([discovery_pipeline])

        self._app_manager.run()
        images_csv = open('images0.csv')
        images = csv.reader(images_csv)
        images.next()
        pre_execs = self._resolve_pre_execs()
        img_pipelines = list()
        idx = 0
        for [image, size] in images:
            img_pipe = self._generate_pipeline(name='P%s' % idx,
                                               pre_execs=pre_execs,
                                               image=image,
                                               image_size=int(size))
            img_pipelines.append(img_pipe)
            idx += 1

        self._app_manager.workflow = set(img_pipelines)

        self._app_manager.run()

    def _terminate(self):
        '''
        Stops the execution
        '''

        self._app_manager.resource_terminate()
