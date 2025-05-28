class PersonValidationError(Exception):
    """Base class for all validation errors in Person."""
    pass

class InvalidIDError(PersonValidationError):
    pass

class InvalidNameError(PersonValidationError):
    pass

class InvalidEmailError(PersonValidationError):
    pass

class InvalidBillingError(PersonValidationError):
    pass

class InvalidLocationError(PersonValidationError):
    pass