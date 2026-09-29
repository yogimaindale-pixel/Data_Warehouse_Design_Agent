# Module docstring explaining data lineage records generation
"""Data lineage generator producing field-level lineage records from source system attributes to target warehouse tables."""

# Import List and Dict type hints
from typing import List, Dict
# Import contract dataclasses
from dw_agent.contracts import DimensionSpec, FactSpec

# Function generating data lineage dictionary records
def generate_lineage_records(dimensions: List[DimensionSpec], facts: List[FactSpec]) -> List[Dict[str, str]]:
    """Construct data lineage records mapping source table/column inputs to target dimension/fact schema outputs.

    Args:
        dimensions (List[DimensionSpec]): Dimension specifications.
        facts (List[FactSpec]): Fact specifications.

    Returns:
        List[Dict[str, str]]: List of lineage dictionary rows.
    """
    lineage = []
    
    # 1. Dimension lineage entries
    for d in dimensions:
        for c in d.columns:
            lineage.append({
                "source_system": "source_db",
                "source_table": d.table_name.replace("dim_", "src_"),
                "source_column": c.name if c.name not in ["effective_date", "expiration_date", "is_current"] else "system_time",
                "target_table": d.table_name,
                "target_column": c.name,
                "transformation": "Direct / SCD"
            })

    # 2. Fact table lineage entries (FK lookups and Measure formulas)
    for f in facts:
        for fk in f.foreign_keys:
            lineage.append({
                "source_system": "source_db",
                "source_table": f.table_name.replace("fact_", "src_"),
                "source_column": fk["col"].replace("_sk", "_id"),
                "target_table": f.table_name,
                "target_column": fk["col"],
                "transformation": f"Dimension SK Lookup ({fk['target_dim']})"
            })
        for m in f.measures:
            lineage.append({
                "source_system": "source_db",
                "source_table": f.table_name.replace("fact_", "src_"),
                "source_column": m.source_column,
                "target_table": f.table_name,
                "target_column": m.name,
                "transformation": m.formula
            })

    return lineage

