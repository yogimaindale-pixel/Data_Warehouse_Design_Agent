# Module docstring explaining business process discovery and fact table classification
"""Business process identifier mapping source tables and requirements to Kimball business processes."""

# Import List type hint
from typing import List
# Import BusinessProcess, Requirement, and SourceTable contract dataclasses
from dw_agent.contracts import Requirement, SourceTable, BusinessProcess

# Function identifying business processes from source tables and requirements
def identify_business_processes(requirements: List[Requirement], source_tables: List[SourceTable]) -> List[BusinessProcess]:
    """Identify business processes suitable for dimensional modeling from source tables and requirements.

    Args:
        requirements (List[Requirement]): List of parsed business requirements.
        source_tables (List[SourceTable]): List of parsed source database tables.

    Returns:
        List[BusinessProcess]: List of proposed BusinessProcess objects.
    """
    processes: List[BusinessProcess] = []
    
    # Map lowercase source table names to table objects for quick lookup
    table_map = {t.name.lower(): t for t in source_tables}
    
    # Process 1: E-commerce Order Placement & Sales (Transaction Fact)
    if "orders" in table_map or "order_items" in table_map or "sales" in table_map:
        processes.append(
            BusinessProcess(
                process_id="BP-001",
                name="Order Placement & Sales",
                triggering_event="Customer places an order line item",
                business_questions=["What is total revenue by product and region?", "Which customer placed the order?"],
                kpis=["Total Sales Amount", "Order Line Quantity", "Average Order Value"],
                source_tables=[t for t in ["orders", "order_items", "customers", "products"] if t in table_map],
                proposed_fact_type="transaction"
            )
        )

    # Process 2: Banking Credit Risk & Loan Performance (Periodic Snapshot Fact)
    if "credit_risk" in table_map or "loans" in table_map or "loan_applications" in table_map or "account_snapshots" in table_map:
        processes.append(
            BusinessProcess(
                process_id="BP-002",
                name="Credit Risk & Loan Performance",
                triggering_event="Daily loan balance and risk snapshot or application decision",
                business_questions=["What is the total exposure by risk rating?", "How many loans are delinquent?"],
                kpis=["Total Outstanding Principal", "Delinquent Loan Count", "Average Credit Score"],
                source_tables=[t for t in ["loans", "loan_applications", "account_snapshots", "borrowers"] if t in table_map],
                proposed_fact_type="periodic_snapshot"
            )
        )

    # Fallback Process: Generic Business Transactions
    if not processes:
        src_names = [t.name for t in source_tables] or ["transactions"]
        processes.append(
            BusinessProcess(
                process_id="BP-001",
                name="Core Business Transactions",
                triggering_event="Business transaction event occurs",
                business_questions=["What is the transaction volume and total amount?"],
                kpis=["Transaction Count", "Total Transaction Amount"],
                source_tables=src_names,
                proposed_fact_type="transaction"
            )
        )

    return processes

