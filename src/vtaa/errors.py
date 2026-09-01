class VTAAError(Exception):
    """Base exception for expected user-facing failures."""


class ValidationError(VTAAError):
    """Raised when a reference bundle violates the versioned contract."""


class ProbeError(VTAAError):
    """Raised when video metadata cannot be read with ffprobe."""

