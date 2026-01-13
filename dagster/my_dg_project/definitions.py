from dagster import Definitions
from dagster_dbt import DbtCliResource
from dagster_duckdb import DuckDBIOManager
from dagster_duckdb_pandas import DuckDBPandasTypeHandler
from .assets import my_project_dbt_assets, python_asset
from .project import dbt_project
from .schedules import schedules

class MyDuckDBIOManager(DuckDBIOManager):  
    @staticmethod  
    def type_handlers():
        return [DuckDBPandasTypeHandler()]  

defs = Definitions(
    assets=[
        my_project_dbt_assets,
        python_asset,
    ],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=dbt_project),
        "duckdb_io_manager": MyDuckDBIOManager(
            database="../dev.duckdb",
            schema="main",
            ),
    },
)