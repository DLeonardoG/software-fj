"""Errors raised by the Software FJ reservation system."""


class SoftwareFJError(Exception):
    """Base error. Callers can catch this one type and keep running."""


class InvalidClientDataError(SoftwareFJError):
    """A personal field is present but does not pass validation."""


class MissingParameterError(SoftwareFJError):
    """A required value was not provided."""


class ServiceUnavailableError(SoftwareFJError):
    """The service exists but is not open for booking."""


class InvalidReservationError(SoftwareFJError):
    """The reservation cannot be created or confirmed."""


class OperationNotAllowedError(SoftwareFJError):
    """The requested change does not match the current state."""


class InconsistentCalculationError(SoftwareFJError):
    """A rate, duration, discount or tax would produce a nonsense total."""
