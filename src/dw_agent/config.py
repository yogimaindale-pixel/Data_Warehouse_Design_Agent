"""Configuration manager for loading YAML settings and platform profiles."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dw_agent.exceptions import ConfigurationError

class ConfigManager:
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config")
        self.config_dir = Path(config_dir)

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        file_path = self.config_dir / filename
        if not file_path.exists():
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            raise ConfigurationError(f"Error loading {file_path}: {e}")

    def load_platform_profile(self, dialect: str) -> Dict[str, Any]:
        profile_path = self.config_dir / "platform_profiles" / f"{dialect.lower()}.yaml"
        if not profile_path.exists():
            raise ConfigurationError(f"Unsupported SQL dialect profile: {dialect}")
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            raise ConfigurationError(f"Error loading platform profile for {dialect}: {e}")

    def get_type_mapping(self, dialect: str) -> Dict[str, str]:
        type_mappings = self.load_yaml("type_mapping.yaml").get("type_mappings", {})
        return type_mappings.get(dialect.lower(), type_mappings.get("sqlite", {}))
