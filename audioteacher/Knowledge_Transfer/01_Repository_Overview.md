# 📌 01. Data Warehouse Design Agent - Repository Overview

## 🎯 Executive Summary & Problem Statement
Designing enterprise Data Warehouses manually takes weeks of data engineering effort, requiring architects to analyze raw source DDLs, infer business processes, establish grain declarations, construct Kimball Bus Matrices, design SCD Type 1/2 dimensions, draft Source-to-Target Mappings (STTM), and generate target DDLs across dialect profiles (SQLite, Snowflake, PostgreSQL, BigQuery).

The **Data Warehouse Design Agent (`dw_agent`)** is an automated, AI-assisted architectural engine that ingests raw source schemas, requirements, and sample datasets to produce 27 production-ready DWH design deliverables in seconds with 100% mathematical and schema traceability.

---

## 🏗️ Architecture & Component Overview

- **01. Discovery Engine** (`inventory.py`, `requirement_parser.py`, `ddl_parser.py`): Ingests raw source SQL DDLs, requirements, and inventory hashes.
- **02. Profiling Engine** (`profiler.py`, `key_discovery.py`, `relationship_discovery.py`, `quality_profiler.py`): Measures nulls, cardinality, foreign keys, and candidate PII columns.
- **03. Modeling Engine** (`business_process.py`, `grain.py`, `bus_matrix.py`, `dimension_designer.py`, `fact_designer.py`): Formulates grains, designs conformed dimensions, facts, and SCD2 policies.
- **04. Generation Engine** (`ddl_generator.py`, `sttm_generator.py`, `etl_spec_generator.py`, `dq_generator.py`, `diagrams.py`, `exporter.py`): Builds target DDLs, STTM workbooks, ERDs, and 27 deliverables.
- **05. Validation Engine** (`model_validator.py`, `sql_validator.py`, `traceability_validator.py`, `acceptance.py`): Enforces grain alignment, zero orphan facts, and SQL syntax rules.

---

## 🛠️ Technology Stack & Dependencies
- **Core Language**: Python 3.10+
- **Data Models & Contracts**: Python `dataclasses` & `dataclasses-json`
- **Data Manipulation & Profiling**: `pandas`, `openpyxl`
- **Configuration & Platform Profiles**: PyYAML (`config/*.yaml`)
- **Documentation & Diagrams**: Mermaid.js (`.mmd`), Markdown, Tabulate
- **CLI & Testing**: `argparse`, `pytest`
