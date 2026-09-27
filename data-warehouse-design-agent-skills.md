---
name: data-warehouse-design-agent
description: Build a Python-only, console-based deterministic Data Warehouse Design Agent that inspects requirements and source metadata, profiles local data, applies dimensional-modeling rules, and generates validated warehouse design deliverables including requirements traceability, business-process and grain decisions, bus matrix, conceptual/logical/physical models, facts, dimensions, SCD policies, DDL, source-to-target mappings, data-quality rules, lineage, ETL specifications, tests, ADRs, and implementation documentation. Use for greenfield or modernization data warehouse design. No web frontend is permitted.
version: 1.0.0
---

# Data Warehouse Design Agent

## 1. Mission
Create a complete, testable, command-line Data Warehouse Design Agent in Python. The agent accepts local requirements and source metadata, executes deterministic modeling rules, records every decision, and writes an implementation-ready warehouse design package.

The agent must be usable by a data architect, modeler, data engineer, ETL developer, tester, BI developer, reviewer, and junior engineer without requiring a browser or graphical frontend.

## 2. Non-Negotiable Constraints

1. Python 3.11 or later.
2. Console and command-line interface only.
3. No Streamlit, React, Angular, Flask UI, Django UI, or other frontend.
4. The default demo must run offline with open-source Python packages.
5. Deterministic design decisions must be implemented as explicit rules and configuration.
6. Optional LLM integration may explain or draft text, but must not silently decide grain, keys, SCD type, relationships, or measures.
7. Every generated design decision must include evidence, source, rule ID, confidence status, and review status.
8. Ambiguous requirements must become assumptions or review questions, not fabricated facts.
9. The agent must never connect to production by default.
10. Generated SQL must be written to files and never executed against an external target unless an explicit safe flag and approved connection are provided.

## 3. Supported Inputs
The agent must scan a user-supplied project folder and accept:

- business requirements: Markdown, TXT, CSV, JSON, YAML
- report and KPI inventory: CSV, XLSX, JSON
- source DDL: SQL
- source metadata: CSV, JSON, YAML
- sample data: CSV, JSON, Parquet, SQLite
- source-to-target mappings: CSV or XLSX
- naming and modeling standards: YAML or Markdown
- data-quality rules: YAML, CSV, or Markdown
- optional existing target DDL and model metadata

For unsupported binary or proprietary formats, generate a clear conversion instruction and continue with all readable inputs.

## 4. Required Console Commands
Implement a Python module invoked as `python -m dw_agent` with commands equivalent to:

```bash
python -m dw_agent init --project <path>
python -m dw_agent inspect --project <path>
python -m dw_agent profile --project <path>
python -m dw_agent design --project <path> --dialect sqlite
python -m dw_agent validate --project <path>
python -m dw_agent report --project <path>
python -m dw_agent demo --scenario ecommerce
python -m dw_agent demo --scenario bfs-credit-risk
python -m dw_agent explain --artifact bus-matrix
python -m dw_agent diff --baseline <path> --candidate <path>
python -m dw_agent clean --project <path>
```

All commands must return meaningful exit codes, structured console logging, and a final output summary.

## 5. Required Repository Structure

```text
project-root/
  README.md
  pyproject.toml
  requirements.txt
  .env.example
  .gitignore
  Makefile
  run_demo.py
  config/
    agent.yaml
    naming_standards.yaml
    modeling_rules.yaml
    type_mapping.yaml
    dq_defaults.yaml
    platform_profiles/
      sqlite.yaml
      postgresql.yaml
      snowflake.yaml
      bigquery.yaml
      synapse.yaml
  inputs/
    requirements/
    source_ddl/
    source_metadata/
    sample_data/
    kpi_inventory/
    standards/
  src/dw_agent/
    __init__.py
    __main__.py
    cli.py
    config.py
    logging.py
    contracts.py
    evidence.py
    exceptions.py
    discovery/
      inventory.py
      requirement_parser.py
      ddl_parser.py
      metadata_loader.py
    profiling/
      profiler.py
      key_discovery.py
      relationship_discovery.py
      quality_profiler.py
    modeling/
      business_process.py
      grain.py
      dimension_designer.py
      fact_designer.py
      scd_policy.py
      bus_matrix.py
      relationship_validator.py
      naming.py
    generation/
      ddl_generator.py
      sttm_generator.py
      etl_spec_generator.py
      dq_generator.py
      lineage_generator.py
      diagrams.py
      documentation.py
    validation/
      model_validator.py
      sql_validator.py
      traceability_validator.py
      acceptance.py
    reporting/
      executive_summary.py
      design_report.py
      review_pack.py
    templates/
  tests/
    unit/
    integration/
    golden/
    scenarios/
  scripts/
    bootstrap.sh
    run_tests.sh
    seed_demo.py
    package_deliverables.py
  output/
```

`output/` is generated and must be safe to delete and regenerate.

## 6. Deterministic Workflow

### Phase 1: Discover
- inventory all project inputs
- calculate file hashes
- identify source systems, tables, columns, primary keys, unique keys, foreign keys, and candidate relationships
- extract business questions, KPIs, filters, dimensions, security requirements, refresh expectations, and history requirements
- create an input-gap report

### Phase 2: Profile
For local sample data calculate:
- row count
- distinct count and uniqueness ratio
- null count and percentage
- minimum and maximum
- numeric distribution summary
- date range
- string length range
- frequent values
- candidate natural keys
- candidate foreign-key coverage
- orphan counts
- duplicate business keys
- potential sensitive-data indicators using configurable name patterns

Never infer sensitive status solely from values. Mark it as a candidate requiring review.

### Phase 3: Identify Business Processes
Create one record per measurable business process. Examples include orders, payments, shipments, balances, claims, lending decisions, transactions, and inventory snapshots.

For every process capture:
- process ID and name
- business owner placeholder
- triggering event
- business questions
- KPIs
- source objects
- proposed fact type
- refresh pattern
- security classification placeholder
- assumptions and open questions

### Phase 4: Declare Grain
The grain must be written as one precise sentence before selecting dimensions or facts.

Examples:
- one row per order line at order placement time
- one row per account per calendar day
- one row per loan application decision
- one row per pipeline execution step

Rules:
- reject vague grain such as “sales data”
- do not mix transaction and snapshot grains in one fact
- identify header versus line-item conflicts
- identify daily versus monthly multi-fact conflicts
- record periodic or accumulating snapshot dates explicitly
- require review if source uniqueness does not support the proposed grain

### Phase 5: Design Dimensions
Support:
- conformed dimensions
- role-playing dimensions
- date and time dimensions
- degenerate dimensions
- junk dimensions
- mini-dimensions
- bridge tables for multivalued relationships
- unknown and not-applicable members
- source natural keys and warehouse surrogate keys
- SCD Types 0, 1, 2, and 3 as initial supported policies

Every dimension design must define:
- grain
- surrogate key
- durable business key
- attributes and types
- source mapping
- SCD policy per attribute
- hierarchy definitions
- default members
- uniqueness rules
- privacy classification placeholder
- retention placeholder

Default to review-required when history requirements are absent. Do not automatically assign SCD2 to every dimension.

### Phase 6: Design Facts
Support:
- transaction fact
- periodic snapshot fact
- accumulating snapshot fact
- factless fact
- aggregate fact or mart

Every fact must define:
- declared grain
- foreign keys
- degenerate dimensions
- measures
- formula and source
- additive behavior by dimension
- currency and unit
- null behavior
- late-arriving-dimension policy
- load pattern
- partition candidate
- expected uniqueness rule

Classify measures as additive, semi-additive, or non-additive. Ratios, percentages, balances, averages, and distinct counts require explicit aggregation guidance.

### Phase 7: Build Enterprise Bus Matrix
Generate a matrix of business processes versus conformed dimensions and include:
- process grain
- fact type
- source systems
- refresh frequency placeholder
- data owner placeholder
- conformance conflicts
- implementation wave recommendation based only on configured scoring

Do not invent owner names, dates, or benefits.

### Phase 8: Generate Physical Design
Generate selectable SQL dialects for SQLite, PostgreSQL, Snowflake, BigQuery, and Synapse.

Required physical features:
- schemas and table names
- surrogate and business keys
- foreign keys where the platform supports them
- SCD columns
- audit columns
- unknown and not-applicable records
- table and column comments where supported
- indexes, clustering, distribution, or partition recommendations as non-executed suggestions
- views for current SCD2 records
- deployment ordering
- rollback scripts for objects created by the agent

Each dialect adapter must be isolated and covered by tests.

### Phase 9: Generate STTM and ETL Specifications
The Source-to-Target Mapping must contain:
- mapping ID
- target table and column
- source system, table, and column
- transformation rule
- lookup rule
- default rule
- rejection behavior
- DQ rule IDs
- SCD behavior
- key-generation behavior
- example input and expected output
- requirement traceability ID

Generate ETL specifications for:
- initial load
- incremental load or CDC
- snapshot comparison
- SCD processing
- dimension-before-fact ordering
- late-arriving dimensions and facts
- restartability
- idempotency
- reconciliation
- quarantine
- backfill
- replay

### Phase 10: Generate Data Quality Rules
Include applicable rules for:
- required fields
- valid types and formats
- key uniqueness
- referential integrity
- domain values
- ranges
- temporal validity
- cross-field consistency
- reconciliation
- grain uniqueness
- SCD overlap and current-row uniqueness
- fact-to-dimension resolution

Every rule must define severity, threshold, action, owner placeholder, and evidence output.

### Phase 11: Validate the Design
Required validations:
- every fact has one declared grain
- all facts and dimensions trace to requirements or documented assumptions
- no direct fact-to-fact relationship
- foreign-key data types match dimension keys
- every SCD2 dimension has validity and current indicators
- no overlapping SCD2 effective periods in test data
- one current SCD2 row per business key
- unknown-member strategy exists
- facts contain no misplaced descriptive attributes unless explicitly justified
- measures are valid at the declared grain
- aggregation behavior is documented
- conformed dimensions use consistent meaning and keys
- STTM targets exist in generated DDL
- DDL names comply with standards
- all generated SQL parses or runs against a safe local engine where applicable
- requirement coverage and unresolved questions are reported

Block final status when critical validation errors exist.

## 7. Rule and Evidence Model
Each deterministic rule must have:

```yaml
id: GRAIN-001
version: 1
priority: 10
category: grain
condition: candidate_key_uniqueness_below_threshold
severity: critical
message: Proposed grain is not unique in profiled sample.
action: require_review
```

Each decision must record:
- decision ID
- rule ID and version
- input evidence references
- output artifact references
- status: proposed, accepted, rejected, superseded
- reviewer placeholder
- timestamp

## 8. Required Deliverables
Generate this package under `output/`:

```text
output/
  00_EXECUTIVE_SUMMARY.md
  01_INPUT_INVENTORY.csv
  02_REQUIREMENTS_CATALOG.csv
  03_OPEN_QUESTIONS_AND_ASSUMPTIONS.md
  04_SOURCE_PROFILE.xlsx
  05_BUSINESS_PROCESS_CATALOG.csv
  06_GRAIN_DECLARATIONS.md
  07_BUS_MATRIX.csv
  08_DIMENSION_CATALOG.xlsx
  09_FACT_CATALOG.xlsx
  10_CONCEPTUAL_MODEL.mmd
  11_LOGICAL_MODEL.mmd
  12_PHYSICAL_MODEL.mmd
  13_TARGET_DDL.sql
  14_ROLLBACK_DDL.sql
  15_STTM.xlsx
  16_ETL_SPECIFICATIONS.md
  17_DATA_QUALITY_RULES.xlsx
  18_LINEAGE.csv
  19_SECURITY_AND_PRIVACY_CONSIDERATIONS.md
  20_PERFORMANCE_DESIGN.md
  21_TEST_CASES.xlsx
  22_REQUIREMENTS_TRACEABILITY_MATRIX.xlsx
  23_ARCHITECTURE_DECISIONS.md
  24_MODEL_VALIDATION_REPORT.md
  25_IMPLEMENTATION_BACKLOG.csv
  26_REVIEW_CHECKLIST.md
  manifest.json
```

If an XLSX writer is unavailable, create equivalent CSV files and report the substitution. Do not create a UI.

## 9. Console User Experience
Use readable console messages:

```text
[DISCOVER] 12 input files found
[PROFILE] 8 source tables profiled
[DESIGN] 3 business processes proposed
[REVIEW] 2 grain decisions need confirmation
[GENERATE] 27 deliverables written
[VALIDATE] PASS=42 WARN=6 FAIL=1
[RESULT] Design package blocked by 1 critical issue
```

Support `--quiet`, `--verbose`, `--json-log`, and `--output` options.

## 10. Security and Governance
- read-only source access by default
- no credentials in repository, console, logs, or artifacts
- `.env.example` contains placeholders only
- parameterized metadata queries
- file-size and row-sampling limits
- configurable masking for sample outputs
- no production data copied into deliverables
- deterministic PII candidate scan using configurable column-name patterns
- audit manifest with input hashes and tool version
- generated artifacts marked draft until reviewed
- no autonomous deployment to production

## 11. Testing Requirements

### Unit Tests
- DDL parsing
- data-type mapping
- candidate-key discovery
- relationship coverage
- business-process extraction
- grain-rule validation
- fact and dimension classification
- SCD policy validation
- bus-matrix creation
- measure additivity classification
- naming standards
- DDL generation per dialect
- STTM referential checks
- deterministic rerun output

### Integration Tests
- requirements plus DDL to full design package
- sample CSV and SQLite profiling
- model to DDL
- model to STTM
- DDL execution in local SQLite for the demo
- invalid design rejected
- clean regeneration of output

### Golden Tests
Given fixed inputs and configuration, normalized deliverable contents must match approved fixtures.

### Scenario Tests
1. E-commerce order-line star schema.
2. BFS credit-risk snapshot and transaction facts.
3. Multi-fact sales, forecast, and budget at different grains.
4. SCD2 customer and product changes.
5. Many-to-many promotion or account relationship using a bridge.
6. Factless eligibility or event coverage.
7. Late-arriving dimension.
8. Schema drift and renamed source column.
9. Ambiguous requirement causing review-required status.
10. Invalid fact-to-fact join causing a critical failure.

## 12. Acceptance Criteria
The project is complete only when:

- a clean bootstrap command succeeds
- no frontend dependency exists
- all required CLI commands display help
- at least two seeded scenarios complete
- the local demo generates all required deliverables
- generated SQLite DDL executes successfully
- facts, dimensions, grain, SCD, STTM, DQ, lineage, and traceability are represented
- critical design errors block completion
- deterministic reruns produce equivalent normalized outputs
- tests pass from one documented command
- README includes exact setup, run, validation, demo, and cleanup commands
- limitations and human-review boundaries are explicit

## 13. Antigravity Execution Plan
Execute without pausing for confirmation:

1. Inspect all existing project files.
2. Create `docs/assumptions.md` with discovered gaps.
3. Scaffold the Python package and CLI.
4. Implement typed contracts and configuration validation.
5. Implement parsers and safe local profiling.
6. Implement rule-based dimensional design.
7. Implement fact, dimension, SCD, and bus-matrix generation.
8. Implement dialect-aware DDL, STTM, ETL, DQ, lineage, and traceability generation.
9. Implement validation and review statuses.
10. Add e-commerce and BFS credit-risk seeded demos.
11. Add unit, integration, golden, and scenario tests.
12. Generate KT-ready documentation and package deliverables.
13. Run clean-room setup, tests, demos, and validation.
14. Report actual results, gaps, and file locations.

## 14. Completion Report
At completion print and save:

- implementation summary
- repository tree
- commands executed
- output files generated
- test results
- demo results
- design warnings and failures
- unresolved assumptions
- supported SQL dialects
- known limitations
- safe next enhancements

Never fabricate performance savings, accuracy, ROI, test results, or requirement coverage.
