select
    md5(concat_ws('|', price_date, premise_code, item_code)) as price_key,
    price_date,
    premise_code,
    item_code,
    price,
    source_month
from {{ ref('stg_pricecatcher') }}