import json
import os
import dagster as dg
import dagster_dbt as dg_dbt
import pandas as pd

from .project import dbt_project


@dg_dbt.dbt_assets(manifest=dbt_project.manifest_path)
def my_project_dbt_assets(context: dg.AssetExecutionContext, dbt: dg_dbt.DbtCliResource):
    dbt_vars: dict[str, bool] = {
        "is_non_python_interacting_dbt_asset_enabled": os.getenv("IS_NON_PYTHON_INTERACTING_DBT_ASSET_ENABLED", "true").lower() == "true"
    }
    dbt_command: list[str] = ["build", "--vars", json.dumps(dbt_vars)]
    yield from dbt.cli(dbt_command, context=context).stream()


@dg.asset(
    deps={
        dg_dbt.get_asset_key_for_model([my_project_dbt_assets], "upstream_of_python_asset")
    },
    description="This is a Python asset that sits in the middle of the dbt DAG.",
    io_manager_key="duckdb_io_manager",
    kinds={"python", "duckdb"},
)
def python_asset() -> pd.DataFrame:
    return pd.DataFrame({"id": [1, 2, 3]})
