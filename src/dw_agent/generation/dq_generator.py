# Module docstring explaining Data Quality (DQ) rules catalog generation
"""Data quality rules catalog generator constructing uniqueness, temporal validity, and referential integrity assertions."""

# Import List type hint
from typing import List
# Import contract dataclasses
from dw_agent.contracts import DimensionSpec, FactSpec, DQRule

# Main DQ rules generation function
def generate_dq_rules(dimensions: List[DimensionSpec], facts: List[FactSpec]) -> List[DQRule]:
    """Generate Data Quality assertions for business keys, SCD2 validity ranges, and fact foreign keys.

    Args:
        dimensions (List[DimensionSpec]): Dimension specifications.
        facts (List[FactSpec]): Fact specifications.

    Returns:
        List[DQRule]: List of DQRule dataclass instances.
    """
    rules: List[DQRule] = []
    rule_idx = 1

    # 1. Dimension Data Quality Rules
    for d in dimensions:
        # Natural Business Key Uniqueness Rule
        rules.append(
            DQRule(
                rule_id=f"DQ-UNIQ-{rule_idx:03d}",
                category="uniqueness",
                target_table=d.table_name,
                target_column=d.business_key,
                condition="COUNT(business_key) = COUNT(DISTINCT business_key)",
                severity="critical",
                threshold="100%",
                action="quarantine"
            )
        )
        rule_idx += 1

        # SCD Type 2 Temporal Validity & Single Active Row Rule
        if d.is_scd2:
            rules.append(
                DQRule(
                    rule_id=f"DQ-SCD2-{rule_idx:03d}",
                    category="temporal_validity",
                    target_table=d.table_name,
                    target_column="effective_date, expiration_date",
                    condition="effective_date < expiration_date AND SUM(is_current=1) = 1 PER business_key",
                    severity="critical",
                    threshold="100%",
                    action="block"
                )
            )
            rule_idx += 1

    # 2. Fact Table Data Quality Rules (Foreign Key Referential Integrity)
    for f in facts:
        for fk in f.foreign_keys:
            rules.append(
                DQRule(
                    rule_id=f"DQ-FK-{rule_idx:03d}",
                    category="referential_integrity",
                    target_table=f.table_name,
                    target_column=fk["col"],
                    condition=f"{fk['col']} IN (SELECT {fk['target_dim'].replace('dim_', '')}_sk FROM {fk['target_dim']}) OR {fk['col']} = -1",
                    severity="critical",
                    threshold="100%",
                    action="quarantine"
                )
            )
            rule_idx += 1

    return rules

