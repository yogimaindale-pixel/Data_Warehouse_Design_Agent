# Discovered Gaps and Design Assumptions

This document records architectural assumptions, default parameters, and design gaps discovered during the setup and implementation of the Data Warehouse Design Agent.

## 1. System & Environment Assumptions
- **Python Version**: Python 3.11+ (verified running Python 3.14).
- **Execution Mode**: Console and CLI only. No web graphical frontend permitted.
- **Dependencies**: Uses Python standard library, `PyYAML`, and `openpyxl` (with fallback to CSV writer if `openpyxl` is missing).
- **Database Engine for Validation**: Local SQLite engine for dry-running and validating target DDL.

## 2. Modeling Engine Assumptions
- **Default SCD Policy**: Dimensions default to SCD Type 1 unless historical tracking is explicitly requested in business requirements or source metadata, in which case SCD Type 2 is assigned.
- **Surrogate Keys**: Integer auto-increment surrogate keys (`<table_name>_sk`) are generated for all dimensional tables across SQL dialects.
- **Durable Business Keys**: Natural business keys (`<table_name>_bk` or domain key) are required for all dimension tables to support SCD processing.
- **Grain Validation**: A candidate grain is considered valid if the sample data or primary key definition achieves 100% uniqueness. If uniqueness is < 100%, the decision status is flagged as `review_required`.
- **Default Unknown Member**: Every dimension includes a default row with `SK = -1` (e.g. `'Unknown'`, `'N/A'`) to handle late-arriving dimensions and missing references.

## 3. Supported Dialects & Mappings
- **Dialects Supported**: SQLite, PostgreSQL, Snowflake, BigQuery, Synapse.
- **Platform Profile Location**: `config/platform_profiles/<dialect>.yaml`.

## 4. Quality Gates & Blocking Rules
- **Critical Failure Conditions**:
  - Fact tables with unstated or ambiguous grain.
  - Direct fact-to-fact joins without an intervening dimension.
  - Non-matching foreign key data types between facts and dimensions.
  - Absence of effective/expiration dates or current flags on SCD2 dimensions.
  - STTM target tables/columns missing from generated DDL.
