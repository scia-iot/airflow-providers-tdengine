"""
Unittest module to test Operators.

Run test:
    python -m unittest tests.operators.test_tdengine -v

"""
import datetime
import unittest
import uuid
from unittest import mock

import pendulum
from airflow import DAG
from airflow.models import TaskInstance
from airflow.utils.state import DagRunState, TaskInstanceState
from airflow.utils.types import DagRunType

from sciaiot.airflow.providers.tdengine.operators.tdengine import CSVImportOperator

DATA_INTERVAL_START = pendulum.datetime(2024, 7, 31, tz="UTC")
DATA_INTERVAL_END = DATA_INTERVAL_START + datetime.timedelta(days=1)

TEST_DAG_ID = uuid.uuid4().hex
TEST_TASK_ID = uuid.uuid4().hex


@mock.patch.dict(
    "os.environ",
    AIRFLOW_CONN_TDENGINE="tdengine://root:taosdata@tdengine:6030/power"
)
class TestCSVImportOperator(unittest.TestCase):
    """
    Test CSVImportOperator.
    """
    def setUp(self):
        with DAG(
            dag_id=TEST_DAG_ID,
            schedule="@daily",
            start_date=DATA_INTERVAL_START
        ) as dag:
            CSVImportOperator(
                task_id=TEST_TASK_ID,
                conn_id="tdengine",
                table_name="meters_airflow_csv_import_test",
                filepath="tests/operators/meters.csv",
            )

        self.dag = dag

    def test_execute_manually(self):
        """ Test execute() manually."""
        dagrun = self.dag.create_dagrun(
            state=DagRunState.RUNNING,
            execution_date=DATA_INTERVAL_START,
            data_interval=(DATA_INTERVAL_START, DATA_INTERVAL_END),
            start_date=DATA_INTERVAL_END,
            run_type=DagRunType.MANUAL,
        )

        ti = dagrun.get_task_instance(TEST_TASK_ID)
        assert ti is not None
        assert isinstance(ti, TaskInstance)

        ti.task = self.dag.get_task(TEST_TASK_ID)
        ti.run(ignore_ti_state=True)
        assert ti.state == TaskInstanceState.SUCCESS
