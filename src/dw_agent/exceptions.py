"""Custom exceptions for the Data Warehouse Design Agent."""

class DWAgentError(Exception):
    """Base exception for DW Agent."""
    pass

class ConfigurationError(DWAgentError):
    """Raised when configuration is invalid or missing."""
    pass

class DiscoveryError(DWAgentError):
    """Raised when discovery fails to find or parse inputs."""
    pass

class ProfilingError(DWAgentError):
    """Raised when profiling fails on sample data."""
    pass

class ValidationError(DWAgentError):
    """Raised when model validation encounters critical errors."""
    pass

class GenerationError(DWAgentError):
    """Raised when artifact generation fails."""
    pass
