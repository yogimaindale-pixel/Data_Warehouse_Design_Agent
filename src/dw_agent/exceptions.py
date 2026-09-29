# Module docstring explaining custom exception hierarchy for the Data Warehouse Design Agent
"""Custom exception classes for structured error handling in Data Warehouse Design Agent."""

# Base exception class for all DW Agent errors
class DWAgentError(Exception):
    """Base exception class for all errors originating within the DW Agent system."""
    pass

# Raised when configuration files (YAML, profiles) are missing or invalid
class ConfigurationError(DWAgentError):
    """Raised when configuration file parsing fails or required settings are missing."""
    pass

# Raised when input discovery fails to locate or parse DDL, metadata, or requirement files
class DiscoveryError(DWAgentError):
    """Raised when input discovery fails to find or parse source artifacts."""
    pass

# Raised when profiling source sample data encounters errors
class ProfilingError(DWAgentError):
    """Raised when data profiling on sample CSV files fails."""
    pass

# Raised when model validation rules encounter critical architectural violations
class ValidationError(DWAgentError):
    """Raised when dimensional model validation encounters blocking errors."""
    pass

# Raised when deliverable generator functions fail during output creation
class GenerationError(DWAgentError):
    """Raised when generating target DDL, STTM, or documentation deliverables fails."""
    pass

