"""Relationship and schema validator for detecting model defects."""

from typing import List
from dw_agent.contracts import DimensionSpec, FactSpec, ValidationItem

def validate_model_relationships(dimensions: List[DimensionSpec], facts: List[FactSpec]) -> List[ValidationItem]:
    items: List[ValidationItem] = []
    dim_map = {d.table_name: d for d in dimensions}

    # Rule 1: Every fact must have foreign keys that exist in dimensions
    for f in facts:
        if not f.foreign_keys:
            items.append(
                ValidationItem(
                    rule_id="REL-002",
                    category="relationship",
                    severity="warning",
                    message=f"Fact table {f.table_name} has no foreign keys defined.",
                    is_pass=False
                )
            )
        for fk in f.foreign_keys:
            target = fk.get("target_dim")
            if target not in dim_map:
                items.append(
                    ValidationItem(
                        rule_id="REL-003",
                        category="relationship",
                        severity="critical",
                        message=f"Fact table {f.table_name} references missing dimension {target}.",
                        is_pass=False,
                        action="block"
                    )
                )

    # Rule 2: Ensure SCD2 dimensions contain validity columns
    for d in dimensions:
        if d.is_scd2:
            col_names = [c.name for c in d.columns]
            if "effective_date" not in col_names or "expiration_date" not in col_names or "is_current" not in col_names:
                items.append(
                    ValidationItem(
                        rule_id="SCD-001",
                        category="scd",
                        severity="critical",
                        message=f"SCD2 dimension {d.table_name} is missing required validity columns (effective_date, expiration_date, is_current).",
                        is_pass=False,
                        action="block"
                    )
                )

    return items
