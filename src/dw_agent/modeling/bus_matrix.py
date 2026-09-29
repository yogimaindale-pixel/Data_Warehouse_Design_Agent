# Module docstring explaining Enterprise Bus Matrix construction
"""Enterprise Bus Matrix builder mapping business processes to conformed dimensions."""

# Import List type hint
from typing import List
# Import contract dataclasses
from dw_agent.contracts import BusinessProcess, DimensionSpec, FactSpec, BusMatrixRow

# Function building the Enterprise Bus Matrix rows
def build_bus_matrix(
    processes: List[BusinessProcess],
    dimensions: List[DimensionSpec],
    facts: List[FactSpec]
) -> List[BusMatrixRow]:
    """Construct Enterprise Bus Matrix mapping every business process against all conformed dimensions.

    Args:
        processes (List[BusinessProcess]): List of business processes.
        dimensions (List[DimensionSpec]): List of dimension specifications.
        facts (List[FactSpec]): List of fact specifications.

    Returns:
        List[BusMatrixRow]: List of BusMatrixRow objects containing dimension participation flags ('Y'/'N').
    """
    rows: List[BusMatrixRow] = []
    dim_names = [d.table_name for d in dimensions]

    for bp in processes:
        fact = next((f for f in facts if f.process_id == bp.process_id), None)
        dim_flags = {}
        
        # Check dimension participation via foreign key references in fact table
        for d_name in dim_names:
            is_participating = "N"
            if fact:
                for fk in fact.foreign_keys:
                    if fk.get("target_dim") == d_name:
                        is_participating = "Y"
            dim_flags[d_name] = is_participating

        rows.append(
            BusMatrixRow(
                process_name=bp.name,
                process_id=bp.process_id,
                fact_type=bp.proposed_fact_type,
                dimensions=dim_flags
            )
        )

    return rows

