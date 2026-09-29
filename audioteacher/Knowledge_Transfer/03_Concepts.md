# 💡 03. Core Engineering Concepts & Pattern Cards

### Concept 1: Automated Dimensional Modeling (Kimball Methodology)
- **What is it?**: Structuring transactional data into conformed Dimensions (descriptive context) and Fact tables (numeric metrics).
- **Why needed?**: Simplifies analytical queries for business users and eliminates multi-table join bottlenecks.
- **Repository Implementation**: `src/dw_agent/modeling/dimension_designer.py` and `fact_designer.py`.

### Concept 2: Kimball Bus Matrix
- **What is it?**: A matrix where rows represent business processes (e.g., Sales, Orders) and columns represent conformed dimensions (e.g., Customer, Product, Date).
- **Repository Implementation**: `src/dw_agent/modeling/bus_matrix.py`.

### Concept 3: Slowly Changing Dimension Type 2 (SCD2)
- **What is it?**: Tracking historical attribute changes by expiring old dimension rows (`effective_to`, `is_current = 0`) and creating new active rows (`effective_from`, `is_current = 1`).
- **Repository Implementation**: `src/dw_agent/modeling/scd_policy.py`.

### Concept 4: Multi-Dialect DDL Code Generation
- **What is it?**: Dynamically compiling conceptual data types (`VARCHAR`, `TIMESTAMP`, `DECIMAL`) into platform-specific SQL (`TEXT` for SQLite, `TIMESTAMP_NTZ` for Snowflake, `DATETIME` for BigQuery).
- **Repository Implementation**: `src/dw_agent/generation/ddl_generator.py` and `config/platform_profiles/*.yaml`.
