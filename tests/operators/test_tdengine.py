"""
Unittest module to test Operators.

Run test:
    python -m unittest tests.operators.test_tdengine -v

"""
import unittest
from unittest import mock

from tdengine.operators.tdengine import CSVImportOperator


@mock.patch.dict(
    "os.environ",
    AIRFLOW_CONN_TDENGINE="tdengine://root:taosdata@tdengine:6030/power"
)
class TestCSVImportOperator(unittest.TestCase):
    """
    Test TDengine Hook.
    """

    def setUp(self):
        self.operator = CSVImportOperator(
            task_id="csv_import",
            conn_id="tdengine",
            table_name="meters_airflow_csv_import_test",
            filepath="tests/operators/meters.csv",
        )

    def test_execute(self):
        """ Test execute()."""
        records = self.operator.execute(context={})

        assert records == 9
