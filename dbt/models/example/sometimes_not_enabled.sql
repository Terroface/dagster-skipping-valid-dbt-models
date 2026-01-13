{{ config(

    enabled=var('is_non_python_interacting_dbt_asset_enabled')

) }}

with source_data as (

    select 1 as id
    union all
    select 2 as id

)

select * from source_data