"""
Unittest module to test Hooks.
"""
import os
import unittest
from unittest import mock

import taos

from sciaiot.airflow.providers.tdengine.hooks.tdengine import TDengineHook, fetch_all


TDENGINE_URI = os.getenv("TDENGINE_URI")

@mock.patch.dict("os.environ", AIRFLOW_CONN_TDENGINE=TDENGINE_URI)
class TestTDengineHook(unittest.TestCase):
    """
    Test TDengine Hook.
    """
    def setUp(self):
        self.hook = TDengineHook("tdengine")

    def test_server_status(self):
        """ Run server_status(). """
        result = self.hook.run("SELECT server_status()", handler=fetch_all)

        assert result is not None
        assert result[0][0] == 1

    def test_show_stables(self):
        """ Run show stables. """
        stables = self.hook.run("SHOW STABLES", handler=fetch_all)

        assert stables is not None
        assert len(stables) >= 1
        assert "meters" in stables[0]
        
    def test_describe_stable(self):
        """ Run describe stable. """
        fields = self.hook.run("DESCRIBE meters", handler=fetch_all)
        
        assert fields is not None
        assert len(fields) >= 1
        
    def test_connection(self):
        """ Test test_connection(). """
        status, message = self.hook.test_connection()
        assert status is True
        assert message == "TDengine is up & running."

    @mock.patch("taos.connect")
    def test_fail_to_connect(self, mocker):
        """ Test test_connection(). """
        mocker.side_effect = taos.ConnectionError("Mocked connection error")

        status, message = self.hook.test_connection()
        assert status is False
        assert message == "Mocked connection error"

        mocker.reset_mock()
