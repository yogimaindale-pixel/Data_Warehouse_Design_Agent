# ❓ 07. Technical Interview Questions & Spoken Response Bank

### Q1: How does the Data Warehouse Design Agent automate Kimball dimensional modeling?
- **30-Second Pitch**: The agent parses raw OLTP DDLs and requirements, identifies business event processes, constructs a Kimball Bus Matrix, and designs conformed dimensions and fact tables automatically.
- **Spoken Response**: "In our Data Warehouse Design Agent, we automate Kimball dimensional modeling by parsing source CREATE TABLE DDLs and requirements files. The discovery module identifies core business entities and transactional event tables. The modeling engine then separates descriptive attributes into conformed dimensions with surrogate keys, assigns measures to fact tables, and generates a Kimball Bus Matrix. This converts manual architecture work that used to take weeks into an automated 5-second compilation pipeline."

### Q2: How do you handle cross-platform SQL DDL generation for Snowflake, BigQuery, and SQLite?
- **30-Second Pitch**: We separate logical data type definitions from physical target dialects using YAML platform profile mappings.
- **Spoken Response**: "We enforce multi-dialect DDL generation through abstract data type contracts and platform profile mapping files in `config/platform_profiles/`. When compiling target DDLs, `ddl_generator.py` maps logical types like `VARCHAR` or `TIMESTAMP` to physical target types—such as `TEXT` for SQLite, `TIMESTAMP_NTZ` for Snowflake, or `DATETIME` for BigQuery. This ensures 100% dialect accuracy without changing the underlying dimensional model."
