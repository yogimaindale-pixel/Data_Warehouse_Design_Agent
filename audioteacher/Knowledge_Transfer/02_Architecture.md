# 🏛️ 02. Data Warehouse Design Agent - System Architecture

## 1. Automated Architecture Pipeline Stages

### Stage 1: Discovery (`src/dw_agent/discovery/`)
- Scans input directory for source DDLs (`.sql`), metadata tables (`.csv`), and requirements (`.txt`).
- Computes SHA-256 hashes for raw input auditability (`inventory.py`).
- Parses column data types, constraints, and primary/foreign keys (`ddl_parser.py`).

### Stage 2: Profiling & Intelligence (`src/dw_agent/profiling/`)
- Analyzes sample datasets to calculate null percentages, cardinality, and uniqueness.
- Infers candidate business keys and relationship foreign keys (`key_discovery.py`).
- Detects sensitive PII candidate columns for compliance masking (`quality_profiler.py`).

### Stage 3: Dimensional Modeling Engine (`src/dw_agent/modeling/`)
- Identifies business processes and event tables (`business_process.py`).
- Formulates grain declarations for facts (`grain.py`).
- Constructs the Kimball Bus Matrix matching facts and conformed dimensions (`bus_matrix.py`).
- Applies SCD Type 1 (overwrite) and SCD Type 2 (effective start/end dates, current flag) policies (`scd_policy.py`).

### Stage 4: Code & Asset Generation (`src/dw_agent/generation/`)
- Generates target DDLs and rollback DDLs per platform profile (`sqlite`, `snowflake`, `bigquery`, `postgresql`).
- Builds Source-To-Target Mapping (STTM) workbooks (`sttm_generator.py`).
- Renders ERD diagrams in Mermaid syntax (`diagrams.py`).

### Stage 5: Rule & Traceability Validation (`src/dw_agent/validation/`)
- Validates grain alignment, surrogate key presence, and zero orphan facts (`model_validator.py`).
- Verifies 100% requirements coverage (`traceability_validator.py`).
- Evaluates SQLite SQL DDL syntax (`sql_validator.py`).
