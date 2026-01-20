import os
from pathlib import Path

from dagster_dbt import DbtProject

dbt_project = DbtProject(
    project_dir=Path(__file__).parent.parent.parent.joinpath("dbt").resolve(),
    generate_cli_args=[
        "parse",
        "--quiet",
        "--vars",
        f'{{"is_non_python_interacting_dbt_asset_enabled": {
            os.getenv("IS_NON_PYTHON_INTERACTING_DBT_ASSET_ENABLED", "true").lower() == "true"
            }}}',
    ]
)
dbt_project.prepare_if_dev()