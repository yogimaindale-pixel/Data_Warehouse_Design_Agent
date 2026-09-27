---
name: data-warehouse-design-agent-knowledge-transfer
description: Analyze a Python console-based Data Warehouse Design Agent repository and generate a complete step-by-step knowledge-transfer package covering project purpose, architecture, command-line operation, configuration, source inspection, profiling, dimensional modeling decisions, facts, dimensions, grain, SCD, bus matrix, DDL, STTM, ETL specifications, data quality, lineage, validation, testing, troubleshooting, security, extension, deployment, support, demonstration, and handover.
version: 1.0.0
---

# Data Warehouse Design Agent Knowledge Transfer

## 1. Objective
Produce an accurate knowledge-transfer package derived from the actual repository. A new junior engineer must be able to install, run, operate, troubleshoot, test, extend, demonstrate, and support the project using only the documentation and approved access.

Do not describe functionality that is not present in the code. Label items as `Implemented`, `Configured`, `Optional`, `Recommended`, or `Not verified`.

## 2. Mandatory Repository Analysis

1. Inventory every top-level file and folder.
2. Identify Python entry points and console commands.
3. Trace configuration loading and validation.
4. Trace one complete design run from input discovery to deliverable packaging.
5. Trace source DDL parsing and data profiling.
6. Trace business-process, grain, dimension, fact, SCD, and bus-matrix decisions.
7. Trace DDL, STTM, ETL, DQ, lineage, and traceability generation.
8. Trace model validation and exit codes.
9. Inspect unit, integration, golden, and scenario tests.
10. Run available bootstrap, help, test, demo, validation, and cleanup commands.
11. Capture sanitized actual outputs.
12. Identify code/documentation inconsistencies.
13. Mark anything not executed as `Not verified`.

## 3. Required KT Folder
Create:

```text
knowledge-transfer/
  00_KT_INDEX.md
  01_PROJECT_DESCRIPTION.md
  02_BUSINESS_PROBLEM_AND_VALUE.md
  03_ARCHITECTURE.md
  04_REPOSITORY_WALKTHROUGH.md
  05_PREREQUISITES_AND_SETUP.md
  06_CONSOLE_COMMAND_REFERENCE.md
  07_INPUT_FORMATS_AND_CONFIGURATION.md
  08_END_TO_END_EXECUTION_FLOW.md
  09_SOURCE_DISCOVERY_AND_PROFILING.md
  10_DIMENSIONAL_MODELING_ENGINE.md
  11_GRAIN_FACTS_DIMENSIONS_AND_SCD.md
  12_BUS_MATRIX_AND_CONFORMANCE.md
  13_DDL_STTM_ETL_AND_DQ_OUTPUTS.md
  14_LINEAGE_TRACEABILITY_AND_ADRS.md
  15_MODEL_VALIDATION_AND_REVIEW.md
  16_OPERATIONS_RUNBOOK.md
  17_TROUBLESHOOTING_GUIDE.md
  18_TESTING_GUIDE.md
  19_SECURITY_PRIVACY_AND_GOVERNANCE.md
  20_EXTENSION_GUIDE.md
  21_RELEASE_DEPLOYMENT_AND_ROLLBACK.md
  22_DEMO_SCRIPT.md
  23_SUPPORT_HANDOVER_CHECKLIST.md
  24_FAQ_AND_GLOSSARY.md
  25_LIMITATIONS_AND_ROADMAP.md
  diagrams/
    system_context.mmd
    component_architecture.mmd
    design_sequence.mmd
    decision_flow.mmd
    artifact_lineage.mmd
  examples/
    sample_agent_config.yaml
    sample_modeling_rule.yaml
    sample_requirement.md
    sample_source_metadata.csv
    sample_console_session.txt
    sample_review_checklist.md
```

## 4. Writing Standard
- Start each document with purpose, audience, and prerequisites.
- Explain concepts in simple language before technical details.
- Include exact repository paths, classes, functions, configuration keys, commands, expected outputs, and failure outputs.
- Use numbered steps for procedures.
- Use Mermaid source for diagrams.
- Do not include secrets, personal data, or production values.
- Replace environment values with placeholders.
- Explain every acronym at first use.
- Add “Why it matters” and “Common mistake” notes.

## 5. Document Requirements

### 00_KT_INDEX.md
Provide role-based learning paths for junior developer, data modeler, data architect, ETL engineer, tester, reviewer, and support engineer. Include reading order, quick links, and completion checklist.

### 01_PROJECT_DESCRIPTION.md
Explain the outcome, boundaries, supported inputs, console-only design, expected users, deliverables, and deterministic-versus-optional-AI boundary.

### 02_BUSINESS_PROBLEM_AND_VALUE.md
Explain manual modeling pain points, inconsistent grain and SCD decisions, repeated DDL/STTM effort, traceability gaps, review delays, reuse potential, and auditable automation. Treat all benefits as hypotheses until measured.

### 03_ARCHITECTURE.md
Document context, components, control flow, artifact flow, configuration, error handling, evidence model, and external dependencies.

### 04_REPOSITORY_WALKTHROUGH.md
Explain every major folder and important file. Include a change map, for example: “To add a dialect, start here; to change a grain rule, start here.”

### 05_PREREQUISITES_AND_SETUP.md
Give exact platform-neutral setup and separate Windows PowerShell, Windows CMD, and Linux/macOS command examples when supported. Cover virtual environment, dependencies, sample data, configuration validation, and clean reset.

### 06_CONSOLE_COMMAND_REFERENCE.md
For every implemented command include syntax, options, input, output, exit codes, examples, and common errors. No frontend instructions.

### 07_INPUT_FORMATS_AND_CONFIGURATION.md
Document all file formats and schemas, required/optional fields, examples, size limits, sampling, precedence, environment configuration, modeling rules, naming rules, type maps, and validation behavior.

### 08_END_TO_END_EXECUTION_FLOW.md
Trace a complete run with code references and generated artifacts. Include a sequence diagram and exact console transcript from a verified demo.

### 09_SOURCE_DISCOVERY_AND_PROFILING.md
Explain DDL parsing, metadata loading, profiling statistics, key detection, relationship detection, limitations, candidate PII flags, and review expectations.

### 10_DIMENSIONAL_MODELING_ENGINE.md
Explain business-process selection, four-step design logic, rule ordering, deterministic evidence, assumptions, open questions, and review states.

### 11_GRAIN_FACTS_DIMENSIONS_AND_SCD.md
Give worked examples for transaction, periodic snapshot, accumulating snapshot, and factless facts; conformed, role-playing, degenerate, junk, mini-dimensions, bridges; and SCD Types 0, 1, 2, and 3. Explain measure additivity and multi-grain pitfalls.

### 12_BUS_MATRIX_AND_CONFORMANCE.md
Explain matrix creation, conformed dimensions, drill-across support, conflicts, implementation waves, and human review.

### 13_DDL_STTM_ETL_AND_DQ_OUTPUTS.md
Walk through every generated artifact and show how designers, developers, testers, and reviewers use it. Explain dialect differences and non-executed recommendations.

### 14_LINEAGE_TRACEABILITY_AND_ADRS.md
Explain requirement-to-model-to-STTM-to-test traceability, architecture decision records, input hashes, and change history.

### 15_MODEL_VALIDATION_AND_REVIEW.md
Explain every critical validation, warning, block condition, status, review checklist, correction workflow, and regeneration process.

### 16_OPERATIONS_RUNBOOK.md
Cover intake, pre-run checks, safe execution, artifact review, approval, packaging, retention, versioning, issue escalation, reruns, and cleanup.

### 17_TROUBLESHOOTING_GUIDE.md
Use symptom, checks, likely cause, safe resolution, and escalation format for:
- command not found
- dependency installation failure
- no inputs found
- unsupported DDL
- malformed metadata
- profiling failure
- proposed grain not unique
- missing business key
- circular or conflicting relationship
- SCD policy missing
- invalid fact-to-fact join
- STTM target absent from DDL
- SQL dialect parse failure
- nondeterministic golden-test difference
- incomplete output package

### 18_TESTING_GUIDE.md
Explain test layers, fixtures, commands, expected results, golden-file updates, adding a scenario, release gates, and how to distinguish a code defect from an invalid design.

### 19_SECURITY_PRIVACY_AND_GOVERNANCE.md
Cover safe input handling, local processing, credentials, masking, sensitive-data candidates, source permissions, artifact classification, audit manifest, review approval, and production execution restrictions.

### 20_EXTENSION_GUIDE.md
Provide exact steps and required tests for adding:
- input parser
- source connector
- profiling statistic
- modeling rule
- dimension pattern
- fact pattern
- SCD type
- SQL dialect
- deliverable generator
- validator
- console command
- demo scenario

### 21_RELEASE_DEPLOYMENT_AND_ROLLBACK.md
Document packaging, versioning, dependency locking, smoke tests, promotion, rollback, and validation. Do not claim cloud deployment if it is absent.

### 22_DEMO_SCRIPT.md
Create a presenter-ready console demonstration:
1. describe the problem
2. show inputs
3. initialize project
4. inspect and profile
5. run design
6. review business processes and grains
7. inspect bus matrix, facts, dimensions, and SCD
8. inspect DDL and STTM
9. run validation
10. show traceability and assumptions
11. inject one invalid design and show blocking behavior
12. package deliverables

Include narration and expected console output.

### 23_SUPPORT_HANDOVER_CHECKLIST.md
Cover repository access, environment, owners as placeholders, setup, demo, rules, dialects, tests, release, backup, issue handling, security, known gaps, and sign-off.

### 24_FAQ_AND_GLOSSARY.md
Include data warehouse, data mart, OLTP, OLAP, grain, fact, dimension, surrogate key, natural key, SCD, conformed dimension, bus matrix, bridge, factless fact, STTM, DDL, CDC, ETL, data quality, lineage, idempotency, ADR, and golden test.

### 25_LIMITATIONS_AND_ROADMAP.md
Separate confirmed limitations, unverified integrations, technical debt, unsupported formats, scalability boundaries, governance gaps, and prioritized enhancements. Do not invent dates.

## 6. Required Hands-On Exercises

### Beginner
- run help and initialize a sample project
- run an e-commerce demo
- identify fact grain and dimensions
- inspect generated DDL and STTM
- read the validation report

### Intermediate
- add a KPI requirement
- add an SCD1 attribute
- add an SCD2 attribute
- add a DQ rule
- regenerate and compare artifacts

### Advanced
- add a periodic snapshot fact
- add a bridge table
- add a new SQL dialect mapping
- add a critical validation rule
- add a golden scenario

Each exercise needs objective, prerequisites, procedure, expected result, validation, and cleanup.

## 7. KT Quality Gate
The KT package is complete only when:

- every implemented console command is documented
- a clean setup and demo have been attempted
- happy path and at least three failure paths are traced
- grain, facts, dimensions, SCD, bus matrix, STTM, DDL, DQ, lineage, and traceability are explained
- extension steps point to actual code
- no hidden frontend dependency exists
- actual test results are reported without fabrication
- unverified items are marked
- security boundaries are explicit
- a junior engineer can independently run and explain the project

## 8. Final KT Status
Report:
- documents created
- code paths reviewed
- commands executed
- tests and demos verified
- gaps and inconsistencies
- unresolved dependencies
- suggested KT agenda
- handover readiness: READY, READY WITH GAPS, or NOT READY, with evidence
