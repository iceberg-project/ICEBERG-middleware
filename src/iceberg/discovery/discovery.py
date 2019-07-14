"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""

import radical.entk as re


class Discovery(object):
    '''
    :Class Discovery:
    This Class is to create the necessary bag of tasks to discover all the
    images
    :Arguments:
        :modules: A list of strings with the modules that need to be loaded.
                  Default value to None
        :paths: A list of strings with the paths of where images are.
                Default value to None
    '''

    def __init__(self, modules=None, paths=None, pre_execs=None):

        self._modules = modules
        self._paths = paths
        self._pre_execs = pre_execs

    def generate_discover_pipeline(self, filetype='csv'):
        '''
        This function takes as an input paths on Bridges and returns a pipeline
        that will provide a file for all the images that exist in that path.
        '''
        pipeline = re.Pipeline()
        pipeline.name = 'Disc'
        stage = re.Stage()
        stage.name = 'Disc-S0'

        if self._paths is None:
            raise RuntimeError('Images paths are not set.')

        # Create the module load list
        modules_load = list()
        if self._modules:
            for module in self._modules:
                tmp_load = 'module load %s' % module
                modules_load.append(tmp_load)

        if self._pre_execs:
            if isinstance(self._pre_execs, list):
                tmp_pre_execs = modules_load + self._pre_execs
            else:
                tmp_pre_execs = modules_load + [self._pre_execs]
        else:
            tmp_pre_execs = modules_load

        for i in range(len(self._paths)):
            task = re.Task()
            task.name = 'Disc-T%d' % i
            task.pre_exec = tmp_pre_execs
            task.executable = 'python'   # Assign executable to the task
            task.arguments = ['image_disc.py', '%s' % self._paths[i],
                              '--filename=images%d' % i,
                              '--filetype=%s' % filetype, '--filesize']
            task.download_output_data = ['images.csv']
            task.upload_input_data = ['image_disc.py']
            task.cpu_reqs = {'processes': 1, 'threads_per_process': 1,
                             'thread_type': 'OpenMP'}
            stage.add_tasks(task)
        # Add Stage to the Pipeline
        pipeline.add_stages(stage)

        return pipeline