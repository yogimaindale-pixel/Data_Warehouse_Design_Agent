# Module docstring explaining atomic grain declaration and sample data uniqueness checking
"""Grain declaration engine enforcing the single-sentence grain declaration rule for every fact table."""

# Import List type hint
from typing import List
# Import contract dataclasses
from dw_agent.contracts import BusinessProcess, GrainDeclaration, ProfileResult, SourceTable
# Import fact table naming formatter
from dw_agent.modeling.naming import format_fact_table_name

# Main grain declaration function constructing GrainDeclaration objects for each business process
def declare_grains(processes: List[BusinessProcess], source_tables: List[SourceTable], profiles: List[ProfileResult]) -> List[GrainDeclaration]:
    """Declare formal single-sentence atomic grains for all proposed fact tables and check sample key uniqueness.

    Args:
        processes (List[BusinessProcess]): List of identified business processes.
        source_tables (List[SourceTable]): List of source table objects.
        profiles (List[ProfileResult]): Data profiling metrics from sample CSV/DB files.

    Returns:
        List[GrainDeclaration]: List of GrainDeclaration objects.
    """
    grains: List[GrainDeclaration] = []
    
    for bp in processes:
        fact_name = format_fact_table_name(bp.name)
        grain_sentence = ""
        keys = []
        is_unique = True

        # Formulate grain sentence based on proposed fact table type
        if bp.proposed_fact_type == "transaction":
            if "order_items" in bp.source_tables:
                grain_sentence = "One row per order line item at order placement time."
                keys = ["order_id", "order_item_id"]
            elif "orders" in bp.source_tables:
                grain_sentence = "One row per customer order at order submission time."
                keys = ["order_id"]
            else:
                grain_sentence = "One row per individual business transaction event."
                keys = ["transaction_id"]
        elif bp.proposed_fact_type == "periodic_snapshot":
            grain_sentence = "One row per loan account per calendar day."
            keys = ["account_id", "snapshot_date"]
        elif bp.proposed_fact_type == "accumulating_snapshot":
            grain_sentence = "One row per loan application tracking milestones from submission to approval."
            keys = ["application_id"]
        else:
            grain_sentence = f"One row per {bp.name.lower()} event record."
            keys = ["id"]

        # Check uniqueness against profiled sample data
        for p in profiles:
            if p.table_name in bp.source_tables:
                for k in keys:
                    if k in p.columns and p.columns[k].get("null_count", 0) > 0:
                        is_unique = False

        grains.append(
            GrainDeclaration(
                process_id=bp.process_id,
                fact_table_name=fact_name,
                grain_sentence=grain_sentence,
                business_keys=keys,
                is_unique=is_unique
            )
        )

    return grains

