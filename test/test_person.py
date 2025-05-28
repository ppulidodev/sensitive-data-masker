import unittest
import sys
import os


from person import Person

from exceptions import (
    InvalidIDError,
    InvalidNameError,
    InvalidEmailError,
    InvalidBillingError,
    InvalidLocationError
)

class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person(1, "John", "john@email.com", 100.0, "Madrid")

    def test_valid_constructor_and_to_list(self):
        expected = [1, "John", "john@email.com", 100.0, "Madrid"]
        self.assertEqual(self.person.to_list(), expected)
        self.assertEqual(len(self.person.to_list()), 5)
        self.assertIsInstance(self.person.to_list(), list)

    def test_edge_case_inputs(self):

        # Billing = 0.00
        person = Person(2, "Ana", "ana@mail.com", 0.00, "Barcelona")
        self.assertEqual(person.billing, 0.00)

        # Email with subdomain and plus
        person = Person(3, "Ana", "ana+smith@mail.co.uk", 50.5, "Paris")
        self.assertEqual(person.email, "ana+smith@mail.co.uk")

        # Location with spaces
        person = Person(4, "Ana", "ana@mail.com", 10.0, "  Paris  ")
        self.assertEqual(person.location, "Paris")

    def test_invalid_inputs_raise_correct_exceptions(self):
        test_cases = [
            # ID
            (InvalidIDError, ("abc", "John", "jonh@email.com", 100.0, "Madrid")),
            (InvalidIDError, ("0", "Paul", "paul@email.com", 100.0, "Madrid")),
            # Name
            (InvalidNameError, (2, "", "mail@email.com", 0.0, "NY")),
            (InvalidNameError, (2, "J0hn", "mail@email.com", 0.0, "NY")),
            # Email
            (InvalidEmailError, (2, "John", "", 0.0, "Paris")),
            (InvalidEmailError, (2, "John", "person-at-email.com", 0.0, "NY")),
            # Billing
            (InvalidBillingError, (2, "Ana", "ana@email.com", -50.0, "Paris")),
            (InvalidBillingError, (2, "Ana", "ana@email.com", 100.123, "Paris")),
            # Location
            (InvalidLocationError, (2, "Josh", "person@email.com", 0.0, "")),
            (InvalidLocationError, (2, "Josh", "person@email.com", 0.0, "Madr1d")),
        ]

        for exception, args in test_cases:
            with self.subTest(args=args):
                with self.assertRaises(exception):
                    Person(*args)

if __name__ == '__main__':
    unittest.main()