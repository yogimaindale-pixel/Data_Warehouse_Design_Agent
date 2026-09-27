"""Fact table designer module."""

from typing import List
from dw_agent.contracts import BusinessProcess, GrainDeclaration, DimensionSpec, FactSpec, FactMeasure, SourceTable
from dw_agent.modeling.naming import format_fact_table_name

def design_facts(
    processes: List[BusinessProcess],
    grains: List[GrainDeclaration],
    dimensions: List[DimensionSpec],
    source_tables: List[SourceTable]
) -> List[FactSpec]:
    facts: List[FactSpec] = []
    dim_map = {d.table_name: d for d in dimensions}

    for bp in processes:
        fact_name = format_fact_table_name(bp.name)
        grain_obj = next((g for g in grains if g.process_id == bp.process_id), None)
        grain_sentence = grain_obj.grain_sentence if grain_obj else "One row per transaction"

        # Dynamically map foreign keys for all available dimensions in dim_map
        fks = []
        for dim_tbl, dim_spec in dim_map.items():
            fks.append({"col": dim_spec.surrogate_key, "target_dim": dim_tbl})

        measures: List[FactMeasure] = []
        degen_dims = []

        if bp.proposed_fact_type == "transaction":
            degen_dims = ["order_id"]
            measures = [
                FactMeasure(name="quantity", formula="SUM(quantity)", source_column="quantity", additivity="additive", agg_guidance="SUM"),
                FactMeasure(name="unit_price", formula="AVG(unit_price)", source_column="unit_price", additivity="non-additive", agg_guidance="AVG"),
                FactMeasure(name="sales_amount", formula="SUM(quantity * unit_price)", source_column="sales_amount", additivity="additive", agg_guidance="SUM"),
                FactMeasure(name="discount_amount", formula="SUM(discount_amount)", source_column="discount_amount", additivity="additive", agg_guidance="SUM")
            ]
        elif bp.proposed_fact_type == "periodic_snapshot":
            degen_dims = ["account_number"]
            measures = [
                FactMeasure(name="outstanding_principal_balance", formula="SUM(principal_balance)", source_column="principal_balance", additivity="semi-additive", agg_guidance="SUM across accounts, LAST across time"),
                FactMeasure(name="accrued_interest", formula="SUM(accrued_interest)", source_column="accrued_interest", additivity="semi-additive", agg_guidance="SUM across accounts, LAST across time"),
                FactMeasure(name="credit_score", formula="AVG(credit_score)", source_column="credit_score", additivity="non-additive", agg_guidance="AVG")
            ]
        elif bp.proposed_fact_type == "accumulating_snapshot":
            degen_dims = ["application_number"]
            measures = [
                FactMeasure(name="requested_amount", formula="SUM(requested_amount)", source_column="requested_amount", additivity="additive", agg_guidance="SUM"),
                FactMeasure(name="approved_amount", formula="SUM(approved_amount)", source_column="approved_amount", additivity="additive", agg_guidance="SUM"),
                FactMeasure(name="processing_duration_days", formula="AVG(days_to_decision)", source_column="days_to_decision", additivity="non-additive", agg_guidance="AVG")
            ]
        else: # factless or generic event
            degen_dims = ["event_id"]
            measures = [
                FactMeasure(name="event_count", formula="COUNT(1)", source_column="event_id", additivity="additive", agg_guidance="COUNT")
            ]

        facts.append(
            FactSpec(
                table_name=fact_name,
                process_id=bp.process_id,
                grain_sentence=grain_sentence,
                fact_type=bp.proposed_fact_type,
                foreign_keys=fks,
                degenerate_dimensions=degen_dims,
                measures=measures
            )
        )

    return facts

