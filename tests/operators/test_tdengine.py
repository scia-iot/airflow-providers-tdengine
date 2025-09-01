"""
Unittest module to test Operators.
"""
import os
import unittest
import uuid
from unittest import mock

import pendulum
from airflow import DAG
from airflow.models import TaskInstance
from airflow.utils.state import DagRunState, TaskInstanceState
from airflow.utils.types import DagRunTriggeredByType, DagRunType

from sciaiot.airflow.providers.tdengine.operators.tdengine import (
    CSVImportOperator,
    STableDescribeOperator,
)

TDENGINE_URI = os.getenv("TDENGINE_URI")
START_DATE = pendulum.datetime(2024, 7, 31, tz="UTC")

TEST_STD_DAG_ID = uuid.uuid4().hex
TEST_STD_TASK_ID = uuid.uuid4().hex
TEST_STD_RUN_ID = uuid.uuid4().hex

@mock.patch.dict("os.environ", {"AIRFLOW_CONN_TDENGINE": TDENGINE_URI})
class TestSTableDescribeOperator(unittest.TestCase):
    """
    Test STableDescribeOperator.
    """

    def setUp(self):
        with DAG(
            dag_id=TEST_STD_DAG_ID, schedule="@daily", start_date=START_DATE
        ) as dag:
            STableDescribeOperator(
                task_id=TEST_STD_TASK_ID,
                conn_id="tdengine",
                stable_name="meters",
            )

        self.dag = dag

    def test_execute_manually(self):
        """Test execute() manually."""
        dagrun = self.dag.create_dagrun(
            run_id=TEST_STD_RUN_ID,
            run_type=DagRunType.MANUAL,
            run_after=START_DATE,
            triggered_by=DagRunTriggeredByType.TIMETABLE,
            state=DagRunState.RUNNING,
        )

        ti = dagrun.get_task_instance(TEST_STD_TASK_ID)
        assert ti is not None
        assert isinstance(ti, TaskInstance)

        ti.task = self.dag.get_task(TEST_STD_TASK_ID)
        ti.run(ignore_ti_state=True)
        assert ti.state == TaskInstanceState.SUCCESS

        # The result is pushed to XComs. Let's check it.
        columns = ti.xcom_pull(task_ids=TEST_STD_TASK_ID, key="return_value")

        expected_columns = [
            {"name": "ts", "type": "datetime", "length": 8},
            {"name": "current", "type": "float", "length": 4},
            {"name": "voltage", "type": "int", "length": 4},
            {"name": "phase", "type": "float", "length": 4},
            {"name": "location", "type": "int", "length": 1},
            {"name": "groupid", "type": "int", "length": 4},
            {'name': 'remarks', 'type': 'bytes', 'length': 128},
        ]

        self.assertEqual(columns, expected_columns)


TEST_CI_DAG_ID = uuid.uuid4().hex
TEST_CI_TASK_ID = uuid.uuid4().hex
TEST_CI_RUN_ID = uuid.uuid4().hex

@mock.patch.dict("os.environ", {"AIRFLOW_CONN_TDENGINE": TDENGINE_URI})
class TestCSVImportOperator(unittest.TestCase):
    """
    Test CSVImportOperator.
    """

    def setUp(self):
        with DAG(
            dag_id=TEST_CI_DAG_ID, schedule="@daily", start_date=START_DATE
        ) as dag:
            CSVImportOperator(
                task_id=TEST_CI_TASK_ID,
                conn_id="tdengine",
                table_name="meters_airflow_csv_import_test",
                filepath="tests/operators/meters.csv",
            )

        self.dag = dag

    def test_execute_manually(self):
        """Test execute() manually."""
        dagrun = self.dag.create_dagrun(
            run_id=TEST_CI_RUN_ID,
            run_type=DagRunType.MANUAL,
            run_after=START_DATE,
            triggered_by=DagRunTriggeredByType.TIMETABLE,
            state=DagRunState.RUNNING,
        )

        ti = dagrun.get_task_instance(TEST_CI_TASK_ID)
        assert ti is not None
        assert isinstance(ti, TaskInstance)

        ti.task = self.dag.get_task(TEST_CI_TASK_ID)
        ti.run(ignore_ti_state=True)
        assert ti.state == TaskInstanceState.SUCCESS
