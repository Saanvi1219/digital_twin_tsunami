"""
Custom exceptions used by the Digital Twin.
"""

class DigitalTwinError(Exception):
    """Base exception for Digital Twin."""
    pass


class ValidationError(DigitalTwinError):
    """Raised when validation fails."""
    pass


class StateError(DigitalTwinError):
    """Raised when the twin state is invalid."""
    pass


class VersionError(DigitalTwinError):
    """Raised when version control fails."""
    pass


class SerializationError(DigitalTwinError):
    """Raised during save/load failures."""
    pass