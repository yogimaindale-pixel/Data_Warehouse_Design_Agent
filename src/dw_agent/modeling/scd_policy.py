# Module docstring explaining Slowly Changing Dimension (SCD) policy application
"""SCD policy module mapping dimension column attributes to their designated SCD management type (SCD 0, 1, or 2)."""

# Import List and Dict type hints
from typing import List, Dict
# Import contract dataclasses
from dw_agent.contracts import DimensionSpec, DimensionColumn

# Function extracting SCD policies for all dimensions
def apply_scd_policies(dimensions: List[DimensionSpec]) -> Dict[str, Dict[str, int]]:
    """Extract mapping of dimension table names and column names to their SCD policy types.

    Args:
        dimensions (List[DimensionSpec]): List of designed dimension specifications.

    Returns:
        Dict[str, Dict[str, int]]: Nested dictionary mapping table -> column -> scd_type (0, 1, or 2).
    """
    policies = {}
    for d in dimensions:
        policies[d.table_name] = {}
        for c in d.columns:
            policies[d.table_name][c.name] = c.scd_type
    return policies

