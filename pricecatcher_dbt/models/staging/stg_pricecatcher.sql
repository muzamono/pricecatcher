select
    cast("date" as date) as price_date,
    premise_code,
    item_code,
    price,
    source_month
from {{ source('raw', 'pricecatcher') }}