with

source_python_asset as (
    select * from {{ source('main', 'python_asset') }}
),

{%  if var('is_non_python_interacting_dbt_asset_enabled') %}
    sometimes_not_enabled as (
        select * from {{ ref('sometimes_not_enabled') }}
    ),
{% endif %}

upstream_of_python_asset as (
    select * from {{ ref('upstream_of_python_asset') }}
),

unioned_data as (

    select * from source_python_asset

    union all

    {%  if var('is_non_python_interacting_dbt_asset_enabled') %}
        select * from sometimes_not_enabled

        union all
    {% endif %}

    select * from upstream_of_python_asset

)

select * from unioned_data