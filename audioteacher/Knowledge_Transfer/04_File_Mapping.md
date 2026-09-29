# 🗺️ 04. Master File, Function, and Line Range Mapping Matrix

| Concept | Target File | Class / Function | Start Line | End Line | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Pipeline Entrypoint** | `src/dw_agent/cli.py` | `run_design_pipeline` | 62 | 227 | Master orchestrator invoking Discovery, Profiling, Modeling, Generation, and Validation. |
| **Data Contracts** | `src/dw_agent/contracts.py` | `SourceTable`, `FactSpec`, `DimensionSpec` | 11 | 188 | Strongly-typed dataclasses for pipeline artifacts. |
| **Config Manager** | `src/dw_agent/config.py` | `ConfigManager` | 16 | 84 | Loads PyYAML rules and platform dialect type mappings. |
| **DDL Parsing** | `src/dw_agent/discovery/ddl_parser.py` | `parse_source_ddl` | 17 | 124 | Parses raw SQL CREATE TABLE DDLs into `SourceTable` dataclasses. |
| **Dimension Modeling** | `src/dw_agent/modeling/dimension_designer.py` | `design_dimensions` | 12 | 127 | Infers dimension tables, business keys, and surrogate keys. |
| **Fact Modeling** | `src/dw_agent/modeling/fact_designer.py` | `design_facts` | 12 | 89 | Identifies additive/non-additive measures and foreign keys. |
| **Kimball Bus Matrix** | `src/dw_agent/modeling/bus_matrix.py` | `build_bus_matrix` | 10 | 50 | Builds bus matrix rows mapping business processes to conformed dimensions. |
| **Target DDL Generator** | `src/dw_agent/generation/ddl_generator.py` | `generate_target_ddl` | 12 | 163 | Compiles dialect-specific SQL DDL statements for target data warehouse. |
| **Deliverable Exporter** | `src/dw_agent/generation/exporter.py` | `export_all_deliverables` | 68 | 158 | Writes all 27 markdown, CSV, Excel, and SQL design deliverables. |
| **Model Validation** | `src/dw_agent/validation/model_validator.py` | `validate_warehouse_design` | 12 | 87 | Evaluates grain consistency, primary key uniqueness, and relationship integrity. |
