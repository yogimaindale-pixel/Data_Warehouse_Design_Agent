"""Enterprise Bus Matrix builder."""

from typing import List
from dw_agent.contracts import BusinessProcess, DimensionSpec, FactSpec, BusMatrixRow

def build_bus_matrix(
    processes: List[BusinessProcess],
    dimensions: List[DimensionSpec],
    facts: List[FactSpec]
) -> List[BusMatrixRow]:
    rows: List[BusMatrixRow] = []
    dim_names = [d.table_name for d in dimensions]

    for bp in processes:
        fact = next((f for f in facts if f.process_id == bp.process_id), None)
        dim_flags = {}
        
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
