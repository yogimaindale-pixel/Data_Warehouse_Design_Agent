"""Comprehensive model validator enforcing quality gates."""

from typing import List
from dw_agent.contracts import DimensionSpec, FactSpec, GrainDeclaration, STTMRow, ValidationItem
from dw_agent.modeling.relationship_validator import validate_model_relationships

def validate_warehouse_design(
    dimensions: List[DimensionSpec],
    facts: List[FactSpec],
    grains: List[GrainDeclaration],
    sttms: List[STTMRow]
) -> List[ValidationItem]:
    items: List[ValidationItem] = []

    # 1. Grain Validation: Every fact table must have a declared grain
    for f in facts:
        g = next((g for g in grains if g.fact_table_name == f.table_name), None)
        if not g or not g.grain_sentence:
            items.append(
                ValidationItem(
                    rule_id="GRAIN-001",
                    category="grain",
                    severity="critical",
                    message=f"Fact table {f.table_name} lacks an explicit single-sentence grain declaration.",
                    is_pass=False,
                    action="block"
                )
            )
        else:
            items.append(
                ValidationItem(
                    rule_id="GRAIN-001",
                    category="grain",
                    severity="info",
                    message=f"Fact table {f.table_name} has explicit grain: '{g.grain_sentence}'",
                    is_pass=True
                )
            )

    # 2. Relationship Validation
    items.extend(validate_model_relationships(dimensions, facts))

    # 3. STTM Coverage Check: Ensure all STTM target columns exist in generated model
    target_cols = set()
    for d in dimensions:
        for c in d.columns:
            target_cols.add(f"{d.table_name}.{c.name}")
        target_cols.add(f"{d.table_name}.{d.surrogate_key}")
        target_cols.add(f"{d.table_name}.{d.business_key}")

    for f in facts:
        for fk in f.foreign_keys:
            target_cols.add(f"{f.table_name}.{fk['col']}")
        for m in f.measures:
            target_cols.add(f"{f.table_name}.{m.name}")

    for sttm in sttms:
        col_ref = f"{sttm.target_table}.{sttm.target_column}"
        if col_ref not in target_cols:
            items.append(
                ValidationItem(
                    rule_id="STTM-001",
                    category="sttm",
                    severity="critical",
                    message=f"STTM target {col_ref} is absent from generated target DDL schema.",
                    is_pass=False,
                    action="block"
                )
            )

    return items
