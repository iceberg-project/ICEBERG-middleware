"""
Author: Ioannis Paraskevakos
License: MIT
Copyright: 2018-2019
"""
# pylint: disable=protected-access, unused-argument, unused-import

import os
import random
import mock

from iceberg.discovery import Discovery


# ------------------------------------------------------------------------------
#
def test_init():
    component = Discovery()
    assert component._modules == None
    assert component._paths == None

    component = Discovery(paths=['test','test'])
    assert component._paths == ['test','test']
    assert component._modules == None
    
    component = Discovery(modules=['test','test'])
    assert component._modules == ['test','test']
    assert component._paths == None

    component = Discovery(modules=['test','test'],paths=['test','test'])
    assert component._modules == ['test','test']
    assert component._paths == ['test','test']