# ⚡ 08. Data Warehouse Design Agent Cheat Sheet

| Operation | Command | Purpose |
| :--- | :--- | :--- |
| **Run Pipeline Demo** | `python3 run_demo.py` | Runs automated design pipeline on e-commerce sample scenario. |
| **Generate DWH Design** | `python3 -m dw_agent --input-dir ./demo_ecommerce --platform sqlite` | Compiles 27 DWH design deliverables for SQLite. |
| **Generate Snowflake DWH**| `python3 -m dw_agent --input-dir ./demo_ecommerce --platform snowflake` | Compiles 27 DWH design deliverables for Snowflake. |
| **Run Unit Tests** | `PYTHONPATH=src pytest tests/` | Executes test suite (23 unit/integration/golden tests). |
