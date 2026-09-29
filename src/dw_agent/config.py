# Module docstring explaining configuration management and YAML profile loading
"""Configuration Manager for loading YAML settings, SQL platform profiles, and data type mappings."""

# Import os module for path joining and environment resolution
import os
# Import PyYAML safe_load for parsing YAML configuration files
import yaml
# Import Path class for object-oriented filesystem manipulation
from pathlib import Path
# Import Dict and Any type hints for type annotations
from typing import Dict, Any
# Import ConfigurationError custom exception
from dw_agent.exceptions import ConfigurationError

# ConfigManager class handling configuration file loading and database dialect platform profiles
class ConfigManager:
    """Manages loading of YAML configurations, platform profiles, and data type mapping rules."""

    # Constructor resolving default or custom configuration directory path
    def __init__(self, config_dir: str = None):
        """Initialize ConfigManager with target configuration directory path.

        Args:
            config_dir (str, optional): Custom configuration directory. Defaults to repo root 'config/'.
        """
        if config_dir is None:
            # Default to repo root 'config/' folder relative to this file
            config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config")
        self.config_dir = Path(config_dir)

    # Function loading a generic YAML file from the configuration directory
    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load and parse a YAML file from the config directory.

        Args:
            filename (str): Target YAML file name (e.g., 'type_mapping.yaml').

        Returns:
            Dict[str, Any]: Parsed dictionary content or empty dict if file does not exist.
        """
        file_path = self.config_dir / filename
        if not file_path.exists():
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            raise ConfigurationError(f"Error loading {file_path}: {e}")

    # Function loading target SQL dialect platform profile (e.g. snowflake, postgresql, bigquery, sqlite, synapse)
    def load_platform_profile(self, dialect: str) -> Dict[str, Any]:
        """Load target SQL platform profile YAML configuration.

        Args:
            dialect (str): Target SQL database dialect (e.g., 'snowflake', 'postgresql', 'sqlite').

        Returns:
            Dict[str, Any]: Platform profile dictionary defining DDL features and syntax rules.

        Raises:
            ConfigurationError: If profile file is missing or unparseable.
        """
        profile_path = self.config_dir / "platform_profiles" / f"{dialect.lower()}.yaml"
        if not profile_path.exists():
            raise ConfigurationError(f"Unsupported SQL dialect profile: {dialect}")
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            raise ConfigurationError(f"Error loading platform profile for {dialect}: {e}")

    # Function retrieving target dialect generic data type conversion rules from type_mapping.yaml
    def get_type_mapping(self, dialect: str) -> Dict[str, str]:
        """Retrieve source-to-target data type conversion mappings for a target SQL dialect.

        Args:
            dialect (str): Target database engine dialect.

        Returns:
            Dict[str, str]: Map of generic data types (e.g., 'VARCHAR', 'INTEGER') to dialect types.
        """
        type_mappings = self.load_yaml("type_mapping.yaml").get("type_mappings", {})
        # Return mapped dialect dictionary, falling back to 'sqlite' if dialect key is omitted
        return type_mappings.get(dialect.lower(), type_mappings.get("sqlite", {}))

