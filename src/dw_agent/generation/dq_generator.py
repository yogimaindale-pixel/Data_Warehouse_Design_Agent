"""Data quality rules catalog generator."""

from typing import List
from dw_agent.contracts import DimensionSpec, FactSpec, DQRule

def generate_dq_rules(dimensions: List[DimensionSpec], facts: List[FactSpec]) -> List[DQRule]:
    rules: List[DQRule] = []
    rule_idx = 1

    for d in dimensions:
        # Business key uniqueness
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
