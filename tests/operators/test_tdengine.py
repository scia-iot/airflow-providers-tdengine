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

from sciaiot.airflow.providers.tdengine.operators.tdengine import CSVImportOperator


TDENGINE_URI = os.getenv("TDENGINE_URI")
START_DATE = pendulum.datetime(2024, 7, 31, tz="UTC")
TEST_DAG_ID = uuid.uuid4().hex
TEST_TASK_ID = uuid.uuid4().hex
TEST_RUN_ID = uuid.uuid4().hex

@mock.patch.dict("os.environ", AIRFLOW_CONN_TDENGINE=TDENGINE_URI)
class TestCSVImportOperator(unittest.TestCase):
    """
    Test CSVImportOperator.
    """
    def setUp(self):
        with DAG(
            dag_id=TEST_DAG_ID,
            schedule="@daily",
            start_date=START_DATE
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
            run_id=TEST_RUN_ID,
            run_type=DagRunType.MANUAL,
            run_after=START_DATE,
            triggered_by=DagRunTriggeredByType.TIMETABLE,
            state=DagRunState.RUNNING,
        )

        ti = dagrun.get_task_instance(TEST_TASK_ID)
        assert ti is not None
        assert isinstance(ti, TaskInstance)

        ti.task = self.dag.get_task(TEST_TASK_ID)
        ti.run(ignore_ti_state=True)
        assert ti.state == TaskInstanceState.SUCCESS
