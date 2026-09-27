# Extension Guide

How to add a new SQL dialect:
1. Create `config/platform_profiles/<dialect>.yaml`.
2. Update `config/type_mapping.yaml`.
3. Add dialect tests in `tests/unit/test_ddl_generator.py`.
