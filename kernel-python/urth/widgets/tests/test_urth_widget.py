# (c) Copyright Jupyter Development Team
# (c) Copyright IBM Corp. 2015

""" Tests for the urth_widget.py module """

import unittest
from IPython.kernel.comm import Comm
from unittest.mock import Mock

from ..urth_widget import *


class TestUrthWidget(unittest.TestCase):

    def test_no_state_msg_on_create(self):
        """should not send a state message when the widget is created"""
        comm = Mock(spec=Comm)
        send = Mock()
        comm.attach_mock(send, 'send')
        widget = UrthWidget(comm=comm)
        assert(send.call_count == 0)