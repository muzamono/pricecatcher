select
    premise_code,
    trim(premise) as premise_name,
    trim(address) as address,
    trim(premise_type) as premise_type,
    trim(state) as state,
    trim(district) as district
from {{ source('raw', 'lookup_premise') }}