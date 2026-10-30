select
    premise_code,
    coalesce(premise_name, 'UNKNOWN PREMISE') as premise_name,
    address,
    coalesce(premise_type, 'UNKNOWN') as premise_type,
    coalesce(state, 'UNKNOWN') as state,
    coalesce(district, 'UNKNOWN') as district
from {{ ref('stg_lookup_premise') }}