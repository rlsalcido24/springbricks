
{{
    config(
        materialized = 'table'
    )
}}


select 
    zero_if_null(c_custkey) as intkey,
    contains("12445",c_name) as namecontains,
    c_address,
    c_nationkey,
    c_phone, 
    to_number(c_acctbal, 10, 5) as cleanacctbal
    c_mktsegment,
    c_comment




from
    snowflake_sample_data.tpch_sf1.customer

