with lookup_items as (

    select
        item_code,
        coalesce(item_name, 'UNKNOWN ITEM') as item_name,
        unit,
        coalesce(item_group, 'UNKNOWN') as item_group,
        coalesce(item_category, 'UNKNOWN') as item_category,
        true as is_in_lookup
    from {{ ref('stg_lookup_item') }}

),

orphan_items as (

    select distinct
        item_code,
        'UNKNOWN ITEM' as item_name,
        cast(null as text) as unit,
        'UNKNOWN' as item_group,
        'UNKNOWN' as item_category,
        false as is_in_lookup
    from {{ ref('stg_pricecatcher') }}
    where item_code not in (select item_code from lookup_items)

)

select * from lookup_items
union all
select * from orphan_items