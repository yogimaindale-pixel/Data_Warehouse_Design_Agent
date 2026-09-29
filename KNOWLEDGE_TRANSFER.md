# Knowledge Transfer (KT) Guide: Data Warehouse Design Agent

Welcome to the **Data Warehouse Design Agent** Knowledge Transfer (KT) Guide! This document is specially written for developers and engineers of all experience levels (including junior developers) to master the concepts, codebase structure, and CLI usage of this project.

---

## 1. Beginner-Friendly Core Concepts

### What is a Data Warehouse?
A Data Warehouse (DW) is a central repository designed for analytical reporting and query performance. Unlike transactional databases (OLTP) optimized for fast inserts/updates, data warehouses (OLAP) optimize for fast aggregation, trend analysis, and historical reporting.

### Key Dimensional Modeling Concepts (Kimball Methodology)

1. **Dimension Tables (`dim_*`)**:
   - Descriptive context tables containing attributes used for filtering, grouping, and labeling (e.g. Customer Name, Product Category, Store Region).
   - Contain a **Surrogate Primary Key** (`customer_sk`, integer primary key) and a **Natural/Business Key** (`customer_id`, source identifier).

2. **Fact Tables (`fact_*`)**:
   - Central measurement tables containing numerical metrics (e.g. Sales Amount, Order Quantity) and Foreign Keys referencing dimension surrogate keys.
   - Every fact row represents a specific physical business event.

3. **Grain**:
   - The precise, single-sentence definition of what one single row in a fact table represents (e.g., *"One row per order line item per transaction date"*).

4. **Slowly Changing Dimensions (SCD)**:
   - **SCD Type 1**: Overwrites attribute values when source data changes (no history maintained).
   - **SCD Type 2**: Creates a new dimension row with effective dates (`effective_date`, `expiration_date`, `is_current`) to preserve historic values over time.

5. **Enterprise Bus Matrix**:
   - A master grid mapping business processes (rows) against conformed dimensions (columns) to guarantee enterprise integration.

6. **Source-to-Target Mapping (STTM)**:
   - A detailed column-by-column blueprint defining how data fields flow from source databases into target data warehouse schemas.

---

## 2. Codebase Sitemap & Navigation Guide

```text
/config/Desktop/Data_Warehouse_Design_Agent/
├── run_demo.py                       # Quick demo runner script
├── src/dw_agent/                     # Core Python source package
│   ├── cli.py                        # Command Line Interface (CLI) entrypoint & options parser
│   ├── config.py                     # Configuration profiles & YAML rules manager
│   ├── contracts.py                  # Dataclasses & typed contracts for all entities
│   ├── discovery/                    # Scans and parses input DDLs, CSVs, and Markdown requirements
│   │   ├── inventory.py              # File scanner & SHA-256 hasher
│   │   ├── ddl_parser.py             # SQL CREATE TABLE parser
│   │   └── requirement_parser.py     # Markdown requirements parser
│   ├── profiling/                    # Sample data statistical profiler & PII scanner
│   ├── modeling/                     # Kimball dimensional modeling rules engine
│   │   ├── business_process.py       # Identifies business processes
│   │   ├── grain.py                  # Enforces grain declarations
│   │   ├── dimension_designer.py     # Designs dimension tables
│   │   ├── fact_designer.py          # Designs fact tables
│   │   └── bus_matrix.py             # Constructs Bus Matrix
│   ├── validation/                   # Quality gate validations & SQLite dry-runner
│   ├── generation/                   # Multi-dialect DDL, STTM, DQ, and deliverable generator
│   └── reporting/                    # Formats validation reports and review checklists
├── scripts/                          # Seeder and packaging helper scripts
│   └── seed_demo.py                  # Generates demo datasets (E-commerce, BFS Credit Risk)
└── tests/                            # Pytest suite (unit, integration, scenarios)
```

---

## 3. Step-by-Step Hands-On Tutorials

### Tutorial 1: Setting Up & Running the E-Commerce Demo

Follow these commands to run your first automated data warehouse design:

```bash
# Step 1: Navigate to repository folder
cd /config/Desktop/Data_Warehouse_Design_Agent

# Step 2: Initialize virtual environment and install dependencies
python3 -m venv venv
./venv/bin/pip install -e .

# Step 3: Run the out-of-the-box e-commerce demo scenario
python3 run_demo.py ecommerce
```

**Output**: The agent will create `./demo_ecommerce/output/` populated with 27 deliverables!

---

### Tutorial 2: Creating and Designing a Custom Project

Want to design a warehouse for your own project? Follow these steps:

```bash
# Step 1: Initialize a new project directory structure
./venv/bin/python3 -m dw_agent init --project ./my_custom_project

# Step 2: Add your source SQL DDL file to inputs/source_ddl/
# e.g., create ./my_custom_project/inputs/source_ddl/schema.sql

# Step 3: Add your business requirements to inputs/requirements/
# e.g., create ./my_custom_project/inputs/requirements/reqs.md

# Step 4: Run the design engine specifying PostgreSQL target dialect
./venv/bin/python3 -m dw_agent design --project ./my_custom_project --dialect postgresql
```

---

### Tutorial 3: Interpreting Quality Gate Reports & Deliverables

After running `design`, inspect the output deliverables:

1. **Check Overall Status**: Open `output/00_EXECUTIVE_SUMMARY.md`.
2. **Review Quality Gates**: Open `output/24_MODEL_VALIDATION_REPORT.md` to ensure all checks marked `PASS`.
3. **Inspect Target SQL DDL**: View `output/13_TARGET_DDL.sql` for your production table statements.
4. **View Entity Relationships**: Open `output/10_CONCEPTUAL_MODEL.mmd` or `12_PHYSICAL_MODEL.mmd` in any Mermaid viewer.

---

## 4. Troubleshooting & Frequently Asked Questions (FAQ)

- **Q: Why did my design fail with `GRAIN-001` error?**
  - **A**: Fact tables require an explicit single-sentence grain declaration. Ensure your requirement files describe what a single row represents.
- **Q: How do I change the default dialect?**
  - **A**: Pass `--dialect snowflake` (or `postgresql`, `sqlite`, `bigquery`, `synapse`) to the `design` CLI subcommand.
- **Q: How do I run the full test suite?**
  - **A**: Run `PYTHONPATH=. ./venv/bin/pytest -v`.
