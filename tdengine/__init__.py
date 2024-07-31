"""Module providing a function printing provider version."""
__version__ = "1.0.0"


def get_provider_info():
    """Function to get provider information."""
    return {
        "package-name": "airflow-providers-tdengine",
        "name": "TDengine",
        "description": "A provider of Apache Airflow for TDengine.",
        "versions": [__version__],
        "connection-types": [
            {
                "connection-type": "tdengine",
                "hook-class-name": "tdengine.hooks.tdengine.TDengineHook"
            }
        ],
    }
