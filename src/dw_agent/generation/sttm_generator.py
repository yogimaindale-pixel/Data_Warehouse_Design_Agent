# Module docstring explaining Source-to-Target Mapping (STTM) row generation
"""STTM mapping generator producing column-level source-to-target field mappings, transformations, lookup rules, and DQ cross-references."""

# Import List type hint
from typing import List
# Import contract dataclasses
from dw_agent.contracts import DimensionSpec, FactSpec, STTMRow

# Main STTM generation function
def generate_sttm_mappings(dimensions: List[DimensionSpec], facts: List[FactSpec]) -> List[STTMRow]:
    """Generate detailed Source-to-Target Mapping (STTM) rows for all dimension attributes and fact measures/FKs.

    Args:
        dimensions (List[DimensionSpec]): Dimension specifications.
        facts (List[FactSpec]): Fact specifications.

    Returns:
        List[STTMRow]: List of constructed STTMRow dataclass instances.
    """
    rows: List[STTMRow] = []
    map_idx = 1

    # 1. Generate STTM mappings for Dimension tables and columns
    for d in dimensions:
        for c in d.columns:
            rows.append(
                STTMRow(
                    mapping_id=f"STTM-DIM-{map_idx:03d}",
                    target_table=d.table_name,
                    target_column=c.name,
                    source_system="source_system",
                    source_table=d.table_name.replace("dim_", "src_"),
                    source_column=c.name if c.name not in ["effective_date", "expiration_date", "is_current"] else "sysdate",
                    transformation="Direct Mapping" if c.scd_type == 1 else "SCD Type 2 History Tracking",
                    lookup_rule="Natural Key Lookup",
                    default_rule="'UNKNOWN' for Nulls",
                    rejection_behavior="Quarantine Record",
                    dq_rule_ids="DQ-NULL-001, DQ-UNIQ-001",
                    scd_behavior=f"SCD Type {c.scd_type}",
                    req_id="REQ-GEN-001"
                )
            )
            map_idx += 1

    # 2. Generate STTM mappings for Fact tables (Foreign Keys and Measures)
    for f in facts:
        # Foreign Key SK Lookups
        for fk in f.foreign_keys:
            rows.append(
                STTMRow(
                    mapping_id=f"STTM-FACT-{map_idx:03d}",
                    target_table=f.table_name,
                    target_column=fk["col"],
                    source_system="source_system",
                    source_table=f.table_name.replace("fact_", "src_"),
                    source_column=fk["col"].replace("_sk", "_id"),
                    transformation="Dimension Surrogate Key Lookup",
                    lookup_rule=f"Lookup {fk['target_dim']} ON natural_key",
                    default_rule="-1 (Unknown Dimension Member)",
                    rejection_behavior="Assign Default SK -1 and Log Warning",
                    dq_rule_ids="DQ-FK-001",
                    scd_behavior="N/A",
                    req_id="REQ-GEN-001"
                )
            )
            map_idx += 1

        # Fact Numeric Measures
        for m in f.measures:
            rows.append(
                STTMRow(
                    mapping_id=f"STTM-FACT-{map_idx:03d}",
                    target_table=f.table_name,
                    target_column=m.name,
                    source_system="source_system",
                    source_table=f.table_name.replace("fact_", "src_"),
                    source_column=m.source_column,
                    transformation=m.formula,
                    lookup_rule="Direct Numeric Mapping",
                    default_rule="0.00",
                    rejection_behavior="Quarantine Invalid Numeric",
                    dq_rule_ids="DQ-RANGE-001",
                    scd_behavior="N/A",
                    req_id="REQ-GEN-001"
                )
            )
            map_idx += 1

    return rows

