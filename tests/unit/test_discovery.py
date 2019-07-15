"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""
# pylint: disable=protected-access, unused-argument, unused-import

import os
import inspect
import mock
import pytest

from iceberg.discovery import Discovery


# ------------------------------------------------------------------------------
#
def test_init():
    """
    Test Class constructor
    """
    component = Discovery()
    assert component._modules is None
    assert component._paths is None
    assert component._pre_execs is None

    component = Discovery(paths=['test', 'test'])
    assert component._paths == ['test', 'test']
    assert component._modules is None
    assert component._pre_execs is None

    component = Discovery(modules=['test', 'test'])
    assert component._modules == ['test', 'test']
    assert component._paths is None
    assert component._pre_execs is None

    component = Discovery(modules=['test', 'test'], paths=['test', 'test'])
    assert component._modules == ['test', 'test']
    assert component._paths == ['test', 'test']
    assert component._pre_execs is None

# ------------------------------------------------------------------------------
#
@mock.patch.object(Discovery, '__init__', return_value=None)
def test_generate_pipeline(mocked_init):
    """
    Test generate pipeline
    """
    module_path = os.path.dirname(inspect.getabsfile(Discovery))
    component = Discovery()
    component._modules = None
    component._paths = ['test']
    component._pre_execs = None

    test_pipeline = component.generate_discover_pipeline()
    assert test_pipeline.name == 'Disc'
    assert len(test_pipeline.stages) == 1
    assert test_pipeline.stages[0].name == 'Disc-S0'
    task_list = list(test_pipeline.stages[0].tasks)
    assert len(test_pipeline.stages[0].tasks) == 1
    for task in task_list:
        assert task.name == 'Disc-T0'
        assert task.pre_exec == []
        assert task.executable == 'python'   # Assign executable to the task
        assert task.arguments == ['image_disc.py', 'test',
                                  '--filename=images0',
                                  '--filetype=csv', '--filesize']
        assert task.download_output_data == ['images0.csv']
        assert task.upload_input_data == [module_path + '/image_disc.py']
        assert task.cpu_reqs == {'process_type': '', 'processes': 1,
                                 'threads_per_process': 1,
                                 'thread_type': 'OpenMP'}

    component = Discovery()
    component._modules = ['test_module']
    component._paths = ['test']
    component._pre_execs = None

    test_pipeline = component.generate_discover_pipeline()
    assert test_pipeline.name == 'Disc'
    assert len(test_pipeline.stages) == 1
    assert test_pipeline.stages[0].name == 'Disc-S0'
    task_list = list(test_pipeline.stages[0].tasks)
    assert len(test_pipeline.stages[0].tasks) == 1
    for task in task_list:
        assert task.name == 'Disc-T0'
        assert task.pre_exec == ['module load test_module']
        assert task.executable == 'python'   # Assign executable to the task
        assert task.arguments == ['image_disc.py', 'test',
                                  '--filename=images0',
                                  '--filetype=csv', '--filesize']
        assert task.download_output_data == ['images0.csv']
        assert task.upload_input_data == [module_path + '/image_disc.py']
        assert task.cpu_reqs == {'process_type': '', 'processes': 1,
                                 'threads_per_process': 1,
                                 'thread_type': 'OpenMP'}

# ------------------------------------------------------------------------------
#
@mock.patch.object(Discovery, '__init__', return_value=None)
def test_generate_pipeline_error(mocked_init):
    """
    Test failure modes of generate pipeline
    """

    component = Discovery()
    component._modules = ['test_module']
    component._paths = None

    with pytest.raises(RuntimeError):
        component.generate_discover_pipeline()
    