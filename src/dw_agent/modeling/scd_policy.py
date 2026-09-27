"""SCD policy module."""

from typing import List, Dict
from dw_agent.contracts import DimensionSpec, DimensionColumn

def apply_scd_policies(dimensions: List[DimensionSpec]) -> Dict[str, Dict[str, int]]:
    policies = {}
    for d in dimensions:
        policies[d.table_name] = {}
        for c in d.columns:
            policies[d.table_name][c.name] = c.scd_type
    return policies
