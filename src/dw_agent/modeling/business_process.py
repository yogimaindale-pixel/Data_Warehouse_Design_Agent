"""Business process identifier."""

from typing import List
from dw_agent.contracts import Requirement, SourceTable, BusinessProcess

def identify_business_processes(requirements: List[Requirement], source_tables: List[SourceTable]) -> List[BusinessProcess]:
    processes: List[BusinessProcess] = []
    
    # Map from source tables or requirements to business processes
    table_map = {t.name.lower(): t for t in source_tables}
    
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

    if not processes:
        # Generic process based on first available table or default
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
