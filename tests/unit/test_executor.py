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

from iceberg.executor.executor import Executor
import radical.utils
import radical.entk

# ------------------------------------------------------------------------------
#
def test_init():
    """
    Test Class constructor
    """
    radical.entk.AppManager = mock.Mock(name='test_appmanager')
    radical.entk.AppManager.resource_desc = {}
    radical.utils.Logger = mock.Mock(return_value='test_logger')
    component = Executor('test', 'my_resource', 30, 5)
    assert component._res_dict == {'resource': 'my_resource',
                                   'walltime': 30,
                                   'cpus': 5,
                                   'gpus': 0,
                                   'schema': 'gsissh'}
    assert component._logger == 'test_logger'

    component = Executor('test', 'my_resource', 30, 5, project='test_prj',
                         queue='test_queue')
    assert component._res_dict == {'resource': 'my_resource',
                                   'walltime': 30,
                                   'cpus': 5,
                                   'gpus': 0,
                                   'schema': 'gsissh',
                                   'project': 'test_prj',
                                   'queue': 'test_queue'}
    assert component._logger == 'test_logger'

    component = Executor('test', 'local.localhost_anaconda', 30, 5, gpus=4,
                         project='test_prj', queue='test_queue')
    assert component._res_dict == {'resource': 'local.localhost_anaconda',
                                   'walltime': 30,
                                   'cpus': 5,
                                   'gpus': 4,
                                   'schema': 'ssh',
                                   'project': 'test_prj',
                                   'queue': 'test_queue'}
    assert component._logger == 'test_logger'
