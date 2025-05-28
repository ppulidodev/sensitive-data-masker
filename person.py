import re
from exceptions import (
    InvalidIDError,
    InvalidNameError,
    InvalidEmailError,
    InvalidBillingError,
    InvalidLocationError
)

class Person:
    """
    Represents a person with validated personal and billing information.

    Attributes:
        id (int): A unique integer identifier.
        name (str): The person's full name.
        email (str): The person's email address.
        billing (float): Billing amount, positive with up to two decimal places.
        location (str): The person's location.
    """
    def __init__(self, _id: int, name: str, email: str, billing: float, location: str):
        """
        Initialize a Person instance with validated fields.
        Raises the corresponding exception when one of those fields is not valid.
        """
        self.id = self._validate_id(_id)
        self.name = self._validate_name(name)
        self.email = self._validate_email(email)
        self.billing = self._validate_billing(billing)
        self.location = self._validate_location(location)

    def to_list(self):
        return [self.id, self.name, self.email, self.billing, self.location]
    
    def _validate_id(self, _id):
        try:
            id_int = int(_id)
            if id_int <= 0:
                raise InvalidIDError(f"ID must be a positive, non-zero integer. Got: {_id}")
        except (ValueError, TypeError):
                raise InvalidIDError(f"ID must be a valid integer. Got: {_id}")
        
        return id_int

    def _validate_name(self, name):
        if not name or not str(name).strip() or re.search(r'\d', str(name)):
            raise InvalidNameError(f"Name must be non-empty and contain no numbers. Got: {name}")
        return str(name).strip()

    def _validate_email(self, email):
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?$', str(email).strip()):
            raise InvalidEmailError(f"Email must have a valid format. Got: {email}")
        return str(email)

    def _validate_billing(self, billing):
        billing_str = str(billing).strip()
        if not re.match(r'^\d+(\.\d{1,2})?$', billing_str):
            raise InvalidBillingError(f"Billing must be a valid positive number with up to 2 decimal places. Got: {billing}")
        return float(billing_str)

    def _validate_location(self, location):
        if not location or not str(location).strip() or re.search(r'\d', str(location)):
            raise InvalidLocationError(f"Location must be non-empty and contain no numbers. Got: {location}")
        return str(location).strip()
