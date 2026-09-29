# 🏛️ 10. Senior Principal Engineer Guide & Extension Architecture

### Extending the Agent with a New Dialect Profile (e.g. Databricks Delta Lake)
1. Add `config/platform_profiles/deltalake.yaml` defining data type mappings (`STRING`, `TIMESTAMP`, `DECIMAL(18,2)`).
2. Register the profile in `src/dw_agent/config.py`.
3. Add dialect syntax rules in `src/dw_agent/generation/ddl_generator.py`.
4. Run `PYTHONPATH=src pytest tests/` to verify zero regression.
