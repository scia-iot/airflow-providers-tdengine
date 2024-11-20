
# Airflow TDengine Provider

The Airflow Provider for [TDengine](https://github.com/taosdata/TDengine).

TODO: will try to merge all changes into [the official repo](https://github.com/apache/airflow/tree/main/providers/src/airflow/providers) later.

## Development

### IDE

Use [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) with VS Code.

### Database

Run the tests/DDL.sql in `taos` CLI to setup a test database.

## Test

In the root folder of project, run:

```shell
pytest .
```

## Build

In the root folder of project, run:

```shell
python -m build
```

## Install

Once the package is built locally, run:

```shell
pip install dist/apache_airflow_providers_tdengine-0.0.1-py3-none-any.whl
```

## References

[Provider packages](https://github.com/apache/airflow/blob/main/contributing-docs/11_provider_packages.rst)

[Airflow Sample Provider](https://github.com/astronomer/airflow-provider-sample)
