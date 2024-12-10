"""
Operators for TDengine.
"""
from functools import cached_property
from typing import Any, NoReturn, Sequence

from airflow.exceptions import AirflowException, AirflowFailException
from airflow.hooks.base import BaseHook
from airflow.models import BaseOperator
from airflow.utils.context import Context

from sciaiot.airflow.providers.tdengine.hooks.tdengine import TDengineHook


class BaseTDengineOperator(BaseOperator):
    """
    This is a base class for TDengine Operator to get a DB Hook.

    The provided method is .get_db_hook(). The default behavior will try to
    retrieve the DB hook based on connection type.
    You can customize the behavior by overriding the .get_db_hook() method.

    :param conn_id: reference to a specific database
    """

    conn_id_field = "conn_id"
    template_fields: Sequence[str] = ("conn_id", "database", "hook_params")

    def __init__(
        self,
        *,
        conn_id: str | None = None,
        database: str | None = None,
        hook_params: dict | None = None,
        retry_on_failure: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.database = database
        self.hook_params = hook_params or {}
        self.retry_on_failure = retry_on_failure

    @cached_property
    def _hook(self):
        conn_id = getattr(self, self.conn_id_field)
        self.log.info("Getting connection for %s.", conn_id)
        conn = BaseHook.get_connection(conn_id)
        if self.database:
            conn.schema = self.database

        hook = TDengineHook(conn_id, connection=conn)
        if not isinstance(hook, TDengineHook):
            raise AirflowException(
                f"You are trying to use `tdengine` with {
                    hook.__class__.__name__},"
                " but its provider does not support it. Please upgrade the provider"
                " to a version that supports `tdengine`. The hook class should be"
                " a subclass of `sciaiot.airflow.providers.tdengine.hooks.TDengineHook`."
                f" Got {hook.__class__.__name__} Hook with class hierarchy"
            )

        return hook

    def _raise_exception(self, exception_string: str) -> NoReturn:
        if self.retry_on_failure:
            raise AirflowException(exception_string)
        raise AirflowFailException(exception_string)

    def get_hook(self) -> TDengineHook:
        """
        Get the database hook for the connection.

        :return: the database hook object.
        """
        return self._hook

    def execute(self, context: Context) -> Any:
        raise NotImplementedError


class CSVImportOperator(BaseTDengineOperator):
    """Exporting data to TDengine from a CSV. """

    def __init__(
        self,
        *,
        table_name: str,
        filepath: str,
        conn_id: str | None = None,
        database: str | None = None,
        **kwargs
    ) -> None:
        super().__init__(conn_id=conn_id, database=database, **kwargs)
        self.statement = f"INSERT INTO {table_name} FILE '{filepath}'"

    def execute(self, context: Context) -> int:
        self.log.info("Executing: %s", self.statement)

        hook = self.get_hook()
        hook.run(statement=self.statement)
        imported_records = hook.affected_rows

        self.log.info("Imported records: %s", imported_records)
        return imported_records
