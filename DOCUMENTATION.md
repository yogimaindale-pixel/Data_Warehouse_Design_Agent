# Technical Requirements, Architecture Specification & Business Rules

## 1. Overview & System Requirements

The **Data Warehouse Design Agent** is a deterministic, console-based Python system designed to automate Kimball-style enterprise data warehouse design. It accepts source DDL scripts, sample data files (CSV, SQLite), business requirements, and metadata, and produces an enterprise design package containing 27 deliverables.

### System Requirements
- **Python Version**: Python 3.11+
- **Core Dependencies**: `pyyaml`, `jinja2`, `openpyxl`, `pytest`
- **Execution Mode**: Console CLI (`python -m dw_agent <command>`)

---

## 2. Architecture & Pipeline Specification

The system follows a modular 6-stage linear pipeline:

```mermaid
flowchart LR
    A[Discovery Phase] --> B[Profiling Phase]
    B --> C[Modeling Phase]
    C --> D[Validation Quality Gates]
    D --> E[Generation Phase]
    E --> F[Reporting & Export]
```

### Module Breakdown
1. **Discovery (`src/dw_agent/discovery/`)**: Scans input files (`inventory.py`), parses Markdown requirements (`requirement_parser.py`), parses SQL DDL schemas (`ddl_parser.py`), and loads YAML metadata (`metadata_loader.py`).
2. **Profiling (`src/dw_agent/profiling/`)**: Profiles sample data files (`profiler.py`), identifies primary key candidates (`key_discovery.py`), screens PII candidates (`quality_profiler.py`), and detects foreign key relationships (`relationship_discovery.py`).
3. **Modeling (`src/dw_agent/modeling/`)**: Identifies business processes (`business_process.py`), enforces single-sentence grains (`grain.py`), designs conformed dimensions (`dimension_designer.py`), designs facts (`fact_designer.py`), maps Bus Matrix (`bus_matrix.py`), applies SCD policies (`scd_policy.py`), and enforces snake_case naming (`naming.py`).
4. **Validation (`src/dw_agent/validation/`)**: Evaluates grain declarations, FK completeness, SCD2 validity flags, STTM column coverage, and dry-runs DDL in SQLite in-memory engine.
5. **Generation (`src/dw_agent/generation/`)**: Generates multi-dialect SQL DDLs (`ddl_generator.py`), STTM mappings (`sttm_generator.py`), ETL specifications (`etl_spec_generator.py`), DQ rules (`dq_generator.py`), lineage graphs (`lineage_generator.py`), Mermaid ER diagrams (`diagrams.py`), and exports outputs (`exporter.py`).
6. **Reporting (`src/dw_agent/reporting/`)**: Formats Executive Summary reports (`design_report.py`) and review sign-off checklists (`review_pack.py`).

---

## 3. Core Business & Dimensional Modeling Rules

### 1. Kimball Star Schema Architecture
- Dimensions use lower `snake_case` with prefix `dim_` (e.g., `dim_customers`).
- Facts use lower `snake_case` with prefix `fact_` (e.g., `fact_order_placement`).
- Dimension surrogate primary keys use integer auto-increment with suffix `_sk` (e.g., `customer_sk`).
- Natural/Business keys use suffix `_bk` or `_id` (e.g., `customer_id`).

### 2. Default Unknown Member (-1)
- Every dimension table contains a default unknown record (`surrogate_key = -1`, `business_key = 'UNKNOWN'`) inserted upon creation.
- Fact table late-arriving dimension lookups default to `-1` to preserve referential integrity without dropping fact events.

### 3. Slowly Changing Dimensions (SCD)
- **SCD Type 1**: Overwrite attributes in-place.
- **SCD Type 2**: Maintain full history tracking with `effective_date`, `expiration_date`, and `is_current` columns. Current active view generated as `v_<dimension>_current`.

### 4. Quality Gate Rules
- **GRAIN-001**: Every fact table must declare an explicit single-sentence grain.
- **REL-003**: Fact foreign keys must resolve to existing dimensions.
- **SCD-001**: SCD2 dimensions must possess `effective_date`, `expiration_date`, and `is_current` flags.
- **STTM-001**: All STTM target columns must exist in target DDL statements.

---

## 4. Deliverable Schemas & Manifest Specification

The output package contains 27 standard deliverables under `output/`:

| File Name | Format | Description |
|---|---|---|
| `00_EXECUTIVE_SUMMARY.md` | Markdown | High-level architectural status and metric summary |
| `01_INPUT_INVENTORY.csv` | CSV | Scanned input files and SHA-256 hashes |
| `02_REQUIREMENTS_CATALOG.csv` | CSV | Parsed requirement items with categories |
| `03_OPEN_QUESTIONS_AND_ASSUMPTIONS.md` | Markdown | Discovered gaps and architectural assumptions |
| `04_SOURCE_PROFILE.xlsx` | Excel/CSV | Data profiling metrics (row count, null %, PII candidate flags) |
| `05_BUSINESS_PROCESS_CATALOG.csv` | CSV | Identified enterprise business processes |
| `06_GRAIN_DECLARATIONS.md` | Markdown | Fact table single-sentence grain statements |
| `07_BUS_MATRIX.csv` | CSV | Enterprise Bus Matrix mapping processes to conformed dimensions |
| `08_DIMENSION_CATALOG.xlsx` | Excel/CSV | Dimension schemas, surrogate keys, business keys, and SCD types |
| `09_FACT_CATALOG.xlsx` | Excel/CSV | Fact schemas, measures, foreign keys, and additivity |
| `10_CONCEPTUAL_MODEL.mmd` | Mermaid | High-level conceptual entity relationship diagram |
| `11_LOGICAL_MODEL.mmd` | Mermaid | Detailed logical entity relationship diagram |
| `12_PHYSICAL_MODEL.mmd` | Mermaid | Physical SQL data type entity relationship diagram |
| `13_TARGET_DDL.sql` | SQL | Multi-dialect target DDL script |
| `14_ROLLBACK_DDL.sql` | SQL | Rollback DROP script |
| `15_STTM.xlsx` | Excel/CSV | Source-to-Target mapping rules |
| `16_ETL_SPECIFICATIONS.md` | Markdown | Pipeline load order and SCD execution specs |
| `17_DATA_QUALITY_RULES.xlsx` | Excel/CSV | Assertions for uniqueness, referential integrity, and SCD2 rules |
| `18_LINEAGE.csv` | CSV | Column-level data lineage trace |
| `19_SECURITY_AND_PRIVACY_CONSIDERATIONS.md` | Markdown | PII screening and RBAC governance recommendations |
| `20_PERFORMANCE_DESIGN.md` | Markdown | Partitioning, indexing, and clustering recommendations |
| `21_TEST_CASES.xlsx` | Excel/CSV | Data warehouse test scenarios |
| `22_REQUIREMENTS_TRACEABILITY_MATRIX.xlsx` | Excel/CSV | Requirement-to-model coverage matrix |
| `23_ARCHITECTURE_DECISIONS.md` | Markdown | Key Architecture Decision Records (ADRs) |
| `24_MODEL_VALIDATION_REPORT.md` | Markdown | Quality gate validation table |
| `25_IMPLEMENTATION_BACKLOG.csv` | CSV | Recommended engineering implementation tasks |
| `26_REVIEW_CHECKLIST.md` | Markdown | Executive sign-off checklist |
| `manifest.json` | JSON | Package generation metadata and execution summary |
