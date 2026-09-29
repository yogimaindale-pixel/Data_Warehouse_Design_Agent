# 🐣 09. Beginner Tutorial: Automated Data Warehouse Generation

Welcome to the beginner hands-on guide for the **Data Warehouse Design Agent**!

### Step 1: Execute the Demo Pipeline
```bash
python3 run_demo.py
```
This command runs the complete 5-stage automated design agent on the `./demo_ecommerce` scenario.

### Step 2: Inspect Output Deliverables
Navigate to `./demo_ecommerce/output/` to inspect the generated design package:
- `10_CONCEPTUAL_MODEL.mmd`: View the Mermaid ERD diagram.
- `13_TARGET_DDL.sql`: View the target data warehouse DDL schema.
- `15_STTM.xlsx`: View the Source-to-Target Mapping workbook.
- `07_BUS_MATRIX.csv`: View the Kimball Bus Matrix.
