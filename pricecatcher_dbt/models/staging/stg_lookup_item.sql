select
    item_code,
    trim(item) as item_name,
    trim(unit) as unit,
    trim(item_group) as item_group,
    trim(item_category) as item_category
from {{ source('raw', 'lookup_item') }}