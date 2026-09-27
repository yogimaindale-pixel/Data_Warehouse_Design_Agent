"""Seeder for e-commerce and BFS credit-risk demo scenarios."""

import os
import csv
import sqlite3

def seed_demo_project(project_path: str, scenario: str = "ecommerce"):
    os.makedirs(os.path.join(project_path, "inputs", "requirements"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "inputs", "source_ddl"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "inputs", "source_metadata"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "inputs", "sample_data"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "inputs", "kpi_inventory"), exist_ok=True)

    if scenario == "ecommerce":
        # Requirements
        with open(os.path.join(project_path, "inputs", "requirements", "ecom_reqs.md"), "w") as f:
            f.write("# E-Commerce Analytical Requirements\n")
            f.write("- Track total revenue and order line quantities by product category and customer region.\n")
            f.write("- Maintain customer address change history using SCD Type 2.\n")
            f.write("- PII Security: Customer email and address must be masked in reporting views.\n")

        # Source DDL
        with open(os.path.join(project_path, "inputs", "source_ddl", "ecom_source.sql"), "w") as f:
            f.write("""
CREATE TABLE customers (
    customer_id VARCHAR(64) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    address VARCHAR(200),
    region VARCHAR(50)
);

CREATE TABLE products (
    product_id VARCHAR(64) PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    unit_price NUMERIC(10,2)
);

CREATE TABLE orders (
    order_id VARCHAR(64) PRIMARY KEY,
    customer_id VARCHAR(64) REFERENCES customers(customer_id),
    order_date DATE,
    total_amount NUMERIC(10,2)
);

CREATE TABLE order_items (
    order_id VARCHAR(64) REFERENCES orders(order_id),
    order_item_id VARCHAR(64),
    product_id VARCHAR(64) REFERENCES products(product_id),
    quantity INT,
    unit_price NUMERIC(10,2),
    PRIMARY KEY (order_id, order_item_id)
);
""")

        # Sample CSV Data
        with open(os.path.join(project_path, "inputs", "sample_data", "customers.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["customer_id", "first_name", "last_name", "email", "address", "region"])
            w.writerow(["CUST-001", "Alice", "Smith", "alice@example.com", "123 Main St", "North"])
            w.writerow(["CUST-002", "Bob", "Jones", "bob@example.com", "456 Oak Ave", "South"])

        with open(os.path.join(project_path, "inputs", "sample_data", "products.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["product_id", "product_name", "category", "unit_price"])
            w.writerow(["PROD-101", "Laptop Pro", "Electronics", "1200.00"])
            w.writerow(["PROD-102", "Wireless Mouse", "Electronics", "25.00"])

        with open(os.path.join(project_path, "inputs", "sample_data", "order_items.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["order_id", "order_item_id", "product_id", "quantity", "unit_price"])
            w.writerow(["ORD-9001", "ITEM-1", "PROD-101", "1", "1200.00"])
            w.writerow(["ORD-9001", "ITEM-2", "PROD-102", "2", "25.00"])

    elif scenario == "bfs-credit-risk":
        # Requirements
        with open(os.path.join(project_path, "inputs", "requirements", "bfs_reqs.md"), "w") as f:
            f.write("# BFS Credit Risk Analytical Requirements\n")
            f.write("- Provide daily snapshot of loan account principal balance, accrued interest, and delinquent loan counts.\n")
            f.write("- Track borrower risk rating changes over time.\n")

        # Source DDL
        with open(os.path.join(project_path, "inputs", "source_ddl", "bfs_source.sql"), "w") as f:
            f.write("""
CREATE TABLE borrowers (
    borrower_id VARCHAR(64) PRIMARY KEY,
    borrower_name VARCHAR(100),
    ssn VARCHAR(20),
    credit_score INT,
    risk_rating VARCHAR(10)
);

CREATE TABLE account_snapshots (
    account_id VARCHAR(64),
    borrower_id VARCHAR(64) REFERENCES borrowers(borrower_id),
    snapshot_date DATE,
    principal_balance NUMERIC(15,2),
    accrued_interest NUMERIC(15,2),
    delinquent_days INT,
    PRIMARY KEY (account_id, snapshot_date)
);
""")

        # Sample SQLite DB
        db_path = os.path.join(project_path, "inputs", "sample_data", "bfs_data.sqlite")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("CREATE TABLE borrowers (borrower_id TEXT PRIMARY KEY, borrower_name TEXT, ssn TEXT, credit_score INT, risk_rating TEXT);")
        cur.execute("INSERT INTO borrowers VALUES ('BW-101', 'John Doe', '999-00-1234', 720, 'A');")
        cur.execute("CREATE TABLE account_snapshots (account_id TEXT, borrower_id TEXT, snapshot_date TEXT, principal_balance REAL, accrued_interest REAL, delinquent_days INT);")
        cur.execute("INSERT INTO account_snapshots VALUES ('ACC-8001', 'BW-101', '2026-09-27', 250000.00, 120.50, 0);")
        conn.commit()
        conn.close()

if __name__ == "__main__":
    import sys
    scen = sys.argv[1] if len(sys.argv) > 1 else "ecommerce"
    seed_demo_project("./sample_project", scen)
    print(f"Seeded demo scenario '{scen}' at ./sample_project")
