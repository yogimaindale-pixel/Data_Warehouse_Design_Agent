# Module docstring explaining dimension table modeling logic
"""Dimension designer module constructing conformed date, customer, product, and loan dimensions."""

# Import List and Dict type hints
from typing import List, Dict
# Import contract dataclasses
from dw_agent.contracts import SourceTable, DimensionSpec, DimensionColumn, Requirement
# Import naming convention helper functions
from dw_agent.modeling.naming import format_dim_table_name, format_surrogate_key, format_business_key

# Main dimension designer function building conformed and role-playing dimensions
def design_dimensions(source_tables: List[SourceTable], requirements: List[Requirement]) -> List[DimensionSpec]:
    """Design warehouse dimension table specifications from source schemas and requirements.

    Args:
        source_tables (List[SourceTable]): List of parsed source tables.
        requirements (List[Requirement]): List of parsed business requirements.

    Returns:
        List[DimensionSpec]: List of generated DimensionSpec objects.
    """
    dimensions: List[DimensionSpec] = []
    tbl_map = {t.name.lower(): t for t in source_tables}

    # 1. Date Dimension (Conformed Dimension)
    date_dim = DimensionSpec(
        table_name="dim_date",
        grain="One row per calendar day",
        surrogate_key="date_sk",
        business_key="full_date",
        dim_type="conformed",
        columns=[
            DimensionColumn(name="full_date", data_type="DATE", scd_type=0, description="Full date"),
            DimensionColumn(name="day_of_week", data_type="VARCHAR(20)", scd_type=0, description="Day name"),
            DimensionColumn(name="day_num_in_month", data_type="INTEGER", scd_type=0, description="Day of month"),
            DimensionColumn(name="month_num", data_type="INTEGER", scd_type=0, description="Month number"),
            DimensionColumn(name="month_name", data_type="VARCHAR(20)", scd_type=0, description="Month name"),
            DimensionColumn(name="quarter_num", data_type="INTEGER", scd_type=0, description="Quarter number"),
            DimensionColumn(name="year_num", data_type="INTEGER", scd_type=0, description="Year number"),
            DimensionColumn(name="is_weekend", data_type="BOOLEAN", scd_type=0, description="Weekend indicator")
        ]
    )
    dimensions.append(date_dim)

    # 2. Customer / Borrower Dimension
    cust_tbl = tbl_map.get("customers") or tbl_map.get("borrowers")
    if cust_tbl:
        dim_name = format_dim_table_name(cust_tbl.name)
        sk_name = format_surrogate_key(dim_name)
        bk_name = format_business_key(dim_name)
        
        # Check requirements for SCD2 history tracking requirement
        is_scd2 = any("scd2" in r.description.lower() or "history" in r.description.lower() or "customer" in r.description.lower() for r in requirements)
        
        cols = [DimensionColumn(name=bk_name, data_type="VARCHAR(64)", scd_type=1, description="Durable customer natural key")]
        for c in cust_tbl.columns:
            if not c.is_pk and c.name.lower() not in ["id", "customer_id", "borrower_id"]:
                scd_t = 2 if (is_scd2 and c.name.lower() in ["address", "email", "credit_score", "risk_rating"]) else 1
                cols.append(DimensionColumn(name=c.name.lower(), data_type=c.data_type, scd_type=scd_t, description=f"Customer {c.name}"))

        # Append SCD2 validity columns if SCD Type 2 is enabled
        if is_scd2:
            cols.extend([
                DimensionColumn(name="effective_date", data_type="TIMESTAMP", scd_type=2, description="SCD2 Effective Date"),
                DimensionColumn(name="expiration_date", data_type="TIMESTAMP", scd_type=2, description="SCD2 Expiration Date"),
                DimensionColumn(name="is_current", data_type="BOOLEAN", scd_type=2, description="SCD2 Current Row Indicator")
            ])

        dimensions.append(
            DimensionSpec(
                table_name=dim_name,
                grain="One row per customer profile state",
                surrogate_key=sk_name,
                business_key=bk_name,
                dim_type="conformed",
                is_scd2=is_scd2,
                columns=cols
            )
        )

    # 3. Product Dimension
    prod_tbl = tbl_map.get("products")
    if prod_tbl:
        dim_name = format_dim_table_name(prod_tbl.name)
        sk_name = format_surrogate_key(dim_name)
        bk_name = format_business_key(dim_name)
        
        cols = [DimensionColumn(name=bk_name, data_type="VARCHAR(64)", scd_type=1, description="Durable product natural key")]
        for c in prod_tbl.columns:
            if not c.is_pk and c.name.lower() not in ["id", "product_id"]:
                cols.append(DimensionColumn(name=c.name.lower(), data_type=c.data_type, scd_type=1, description=f"Product {c.name}"))

        dimensions.append(
            DimensionSpec(
                table_name=dim_name,
                grain="One row per product catalog item",
                surrogate_key=sk_name,
                business_key=bk_name,
                dim_type="conformed",
                is_scd2=False,
                columns=cols
            )
        )

    # 4. Loan Product / Risk Rating Dimension
    loan_tbl = tbl_map.get("loans") or tbl_map.get("loan_applications")
    if loan_tbl and not cust_tbl and not prod_tbl:
        dim_name = "dim_loan_product"
        sk_name = "loan_product_sk"
        bk_name = "loan_product_bk"
        dimensions.append(
            DimensionSpec(
                table_name=dim_name,
                grain="One row per loan product type",
                surrogate_key=sk_name,
                business_key=bk_name,
                dim_type="conformed",
                is_scd2=False,
                columns=[
                    DimensionColumn(name=bk_name, data_type="VARCHAR(64)", scd_type=1, description="Product Code"),
                    DimensionColumn(name="product_type", data_type="VARCHAR(100)", scd_type=1, description="Product Description"),
                    DimensionColumn(name="interest_rate_tier", data_type="VARCHAR(50)", scd_type=1, description="Rate Tier")
                ]
            )
        )

    return dimensions

