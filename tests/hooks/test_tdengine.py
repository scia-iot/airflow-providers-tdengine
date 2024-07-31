"""
Unittest module to test Hooks.

Requires the unittest, pytest Python libraries.

Run test:
    python -m unittest tests.hooks.test_tdengine -v
"""

import unittest
from unittest import mock

import taos

from tdengine.hooks.tdengine import TDengineHook, fetch_last


@mock.patch.dict(
    "os.environ", 
    AIRFLOW_CONN_TDENGINE="tdengine://root:taosdata@tdengine:6030/power"
)
class TestTDengineHook(unittest.TestCase):
    """
    Test TDengine Hook.
    """
    def setUp(self):
        self.hook = TDengineHook("tdengine")

    def test_server_status(self):
        """ Run server_status(). """
        result = self.hook.run("SELECT server_status()", handler=fetch_last)

        assert result is not None
        assert result[0] == 1

    def test_show_stables(self):
        """ Run show_stables(). """
        stables = self.hook.run("SHOW STABLES", handler=fetch_last)

        assert stables is not None
        assert len(stables) >= 1

        if "meters" not in stables:
            raise AssertionError("The table 'meters' not found!")

    @mock.patch("taos.connect")
    def test_fail_to_connect(self, mocker):
        """ Test test_connection(). """
        mocker.side_effect = taos.ConnectionError("Mocked connection error")

        status, message = self.hook.test_connection()
        assert status is False
        assert message == "Mocked connection error"

        mocker.reset_mock()
