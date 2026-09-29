# Module docstring explaining dimensional relationship and integrity validation rules
"""Relationship and schema validator verifying target foreign key existence and required SCD2 validity columns."""

# Import List type hint
from typing import List
# Import contract dataclasses
from dw_agent.contracts import DimensionSpec, FactSpec, ValidationItem

# Master function validating dimensional model relationship integrity
def validate_model_relationships(dimensions: List[DimensionSpec], facts: List[FactSpec]) -> List[ValidationItem]:
    """Validate that foreign key references resolve to existing dimensions and SCD2 dimensions contain validity flags.

    Args:
        dimensions (List[DimensionSpec]): Designed dimension specifications.
        facts (List[FactSpec]): Designed fact specifications.

    Returns:
        List[ValidationItem]: List of validation results (PASS or FAIL items).
    """
    items: List[ValidationItem] = []
    dim_map = {d.table_name: d for d in dimensions}

    # Rule 1: Every fact table must define foreign keys that resolve to valid existing dimensions
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

    # Rule 2: Ensure all SCD Type 2 dimensions contain required temporal validity columns
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

