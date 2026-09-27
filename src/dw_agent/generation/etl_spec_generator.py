"""ETL specifications markdown generator."""

from typing import List
from dw_agent.contracts import DimensionSpec, FactSpec

def generate_etl_specifications(dimensions: List[DimensionSpec], facts: List[FactSpec]) -> str:
    lines = []
    lines.append("# ETL Architecture & Load Specifications\n")
    lines.append("## 1. Load Execution Order")
    lines.append("1. **Stage Processing**: Extract source data into staging schemas with timestamp auditing.")
    lines.append("2. **Dimension Processing**: Load conformed and role-playing dimensions before facts to populate surrogate keys.")
    lines.append("3. **Fact Processing**: Lookup dimension surrogate keys and load fact tables.")
    lines.append("4. **Reconciliation & DQ Check**: Validate row counts, totals, and foreign key integrity.\n")

    lines.append("## 2. Dimension Load Specifications (SCD Processing)")
    for d in dimensions:
        lines.append(f"### {d.table_name}")
        lines.append(f"- **Grain**: {d.grain}")
        lines.append(f"- **Durable Key**: `{d.business_key}`")
        if d.is_scd2:
            lines.append("- **SCD Strategy**: Type 2 (History Tracking)")
            lines.append("  - Expire existing active row (`is_current = TRUE` -> `FALSE`, `expiration_date = CURRENT_TIMESTAMP`).")
            lines.append("  - Insert new row with `is_current = TRUE`, `effective_date = CURRENT_TIMESTAMP`, `expiration_date = '9999-12-31'`.")
        else:
            lines.append("- **SCD Strategy**: Type 1 (Overwrite In-Place)")
            lines.append("  - Upsert on natural key match.\n")

    lines.append("## 3. Fact Load Specifications & Late-Arriving Dimensions")
    for f in facts:
        lines.append(f"### {f.table_name}")
        lines.append(f"- **Fact Type**: {f.fact_type}")
        lines.append(f"- **Declared Grain**: {f.grain_sentence}")
        lines.append("- **Late-Arriving Dimension Strategy**: If dimension lookup fails, assign `SK = -1` (Unknown) and log record in quarantine table for backfill reprocessing.")
        lines.append("- **Idempotency & Restartability**: All loads execute via staging MERGE/UPSERT or DELETE-INSERT on batch partition ID.\n")

    return "\n".join(lines)
