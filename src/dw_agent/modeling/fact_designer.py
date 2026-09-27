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

        fks = []
        # Foreign keys to dimensions
        if "dim_date" in dim_map:
            fks.append({"col": "date_sk", "target_dim": "dim_date"})
        if "dim_customers" in dim_map:
            fks.append({"col": "customer_sk", "target_dim": "dim_customers"})
        if "dim_borrowers" in dim_map:
            fks.append({"col": "borrower_sk", "target_dim": "dim_borrowers"})
        if "dim_products" in dim_map:
            fks.append({"col": "product_sk", "target_dim": "dim_products"})
        if "dim_loan_product" in dim_map:
            fks.append({"col": "loan_product_sk", "target_dim": "dim_loan_product"})

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
