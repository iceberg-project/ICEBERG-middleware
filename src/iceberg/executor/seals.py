"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""

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
        :bands: string with bands seperated by commas. defaults to 0 for the panchromatic band
        :stride: distance between tiles as a multiple of patch_size. defaults to 1.0, i.e. adjacent tiles without overlap
        :patch_size: side dimensions for each patch. patches are required to be squares.
        :geotiff: boolean for whether to keep geographical information.
        :model_arch: model architecture, must be a member of models dictionary
        :hyperparam_set: combination of hyperparameters used, must be a member of hyperparameters dictionary
        :model_name: name of input model file from training, this name will also be used in subsequent steps of the pipeline
        :models_folder: folder where the model tar file is saved
    '''
    # pylint: disable=too-many-arguments
    def __init__(self, name, resources, project, input_path, output_path, bands,
                 stride, patch_size, geotiff, model_arch, hyperparam_set,
                 model_name, models_folder):

        super(Seals, self).__init__(name=name,
                                    resource=resources['resource'],
                                    queue=resources['queue'],
                                    walltime=resources['walltime'],
                                    cpus=resources['cpus'],
                                    gpus=resources['gpus'],
                                    project=project)
        self._data_input_path = input_path
        self._output_path = output_path
        self._bands = bands
        self._stride = stride
        self._patch_size = patch_size
        self._geotiff = geotiff
        self._model_name = model_name
        self._model_path = models_folder
        self._model_arch = model_arch
        self._hyperparam = hyperparam_set
        self._req_modules = None
        self._pre_execs = None
        self._env_var = os.environ.get('VE_SEALS')
        if self._res_dict['resource'] == 'xsede.bridges2':

            self._req_modules = ['cuda/10.2.0', 'anaconda3']

            self._pre_execs = ['source activate %s' % self._env_var,
                               'export PYTHONPATH=%s/' % self._env_var
                               + 'lib/python3.9/site-packages']

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

    # pylint: disable=unused-argument
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
        stage0.name = '%s.S0' % (name)
        # Create Task 1, training
        task0 = re.Task()
        task0.name = '%s.T0' % stage0.name
        task0.pre_exec = pre_execs
        task0.executable = 'iceberg_seals.tiling'  # Assign tak executable
        # Assign arguments for the task executable
        task0.arguments = ['--input_image=%s' % image.split('/')[-1],
                           '--output_folder=$NODE_LFS_PATH/%s' % task0.name,
                           '--bands=%s' % self._bands,
                           '--stride=%s' % self._stride,
                           '--patch_size=%s' % self._patch_size,
                           '--geotiff=%s' % self._geotiff]
        task0.link_input_data = [image]
        task0.cpu_reqs = {'cpu_processes': 1, 'cpu_threads': 4,
                          'cpu_process_type': None, 'cpu_thread_type': 'OpenMP'}
        task0.lfs_per_process = image_size

        stage0.add_tasks(task0)
        # Add Stage to the Pipeline
        entk_pipeline.add_stages(stage0)

        # Create a Stage object
        stage1 = re.Stage()
        stage1.name = '%s.S1' % (name)
        # Create Task 1, training
        task1 = re.Task()
        task1.name = '%s.T1' % stage1.name
        task1.pre_exec = pre_execs
        task1.executable = 'iceberg_seals.predicting'  # Assign task executable
        # Assign arguments for the task executable
        task1.arguments = ['--input_dir=$NODE_LFS_PATH/%s' % task0.name,
                           '--model_architecture=%s' % self._model_arch,
                           '--hyperparameter_set=%s' % self._hyperparam,
                           '--model_name=%s' % self._model_name,
                           '--models_folder=./',
                           '--output_dir=./%s' % image.split('/')[-1].split('.')[0],]
        task1.link_input_data = ['$SHARED/%s' % self._model_name]
        task1.cpu_reqs = {'cpu_processes': 1, 'cpu_threads': 1,
                          'cpu_process_type': None, 'cpu_thread_type': 'OpenMP'}
        task1.gpu_reqs = {'gpu_processes': 1, 'gpu_threads': 1,
                          'gpu_process_type': None, 'gpu_thread_type': 'OpenMP'}
        # Download resulting images
        # task1.download_output_data = ['%s/ > %s' % (image.split('/')[-1].
        #                                            split('.')[0],
        #                                            image.split('/')[-1])]
        task1.tags = {'colocate': task0.name}

        stage1.add_tasks(task1)
        # Add Stage to the Pipeline
        entk_pipeline.add_stages(stage1)

        return entk_pipeline

    # pylint: enable=unused-argument
    def _run_workflow(self):
        '''
        Private method that creates and executes the workflow of the use case.
        '''
        self._logger.debug('Uploading shared data %s' % os.path.abspath(self._model_path
                                                          + self._model_name))
        self._app_manager.shared_data = [os.path.abspath(self._model_path
                                                         + self._model_name)]
        discovery = Discovery(modules=self._req_modules,
                              paths=self._data_input_path,
                              pre_execs=self._pre_execs + ['module list',
                                                           'echo $PYTHONPATH',
                                                           'which python'])
        discovery_pipeline = discovery.generate_discover_pipe()

        self._app_manager.workflow = set([discovery_pipeline])

        self._app_manager.run()
        images_csv = open('images0.csv')
        images = csv.reader(images_csv)
        _ = next(images)
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
