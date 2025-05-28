import unittest
import os
from person import Person
from utils import *

class TestUtils(unittest.TestCase):

    def setUp(self):
        with open('test.csv', 'w') as f:
            f.write("ID,Name,Email,Billing,Location\n")
            f.write("1,John Doe,john@example.com,100.0,New York\n")
            f.write("2,Jane Smith,jane@example.com,200.0,London\n")

    def tearDown(self):
        for file in ['test.csv', 'test_write.csv']:
            if os.path.exists(file):
                os.remove(file)

    # --- mask_letters_clean ---
    def test_mask_letters_clean(self):
        self.assertEqual(mask_letters_clean("John"), "XXXX")
        self.assertEqual(mask_letters_clean("Mary Jane"), "XXXX XXXX")
        self.assertEqual(mask_letters_clean("O'Connor"), "X'XXXXXX")
        self.assertEqual(mask_letters_clean("  Mary   Jane  "), "XXXX XXXX")
        self.assertEqual(mask_letters_clean(""), "")

    # --- mask_email ---
    def test_mask_email(self):
        self.assertEqual(mask_email("john@mail.com"), "XXXX@XXXX.com")
        self.assertEqual(mask_email("john.doe+tag@mail.com"), "XXXX.XXX+XXX@XXXX.com")
        self.assertEqual(mask_email("user@mail.co.uk"), "XXXX@XXXX.co.uk")
        self.assertEqual(mask_email("123@456.com"), "123@456.com")

    # --- calculate_billing_average ---
    def test_calculate_billing_average(self):
        people = [
            Person("1", "Alice", "alice@mail.com", 100.0, "Paris"),
            Person("2", "Bob", "bob@mail.com", 200.0, "London")
        ]
        self.assertEqual(calculate_billing_average(people), 150.0)

        self.assertEqual(calculate_billing_average([]), 0.0)

        single = [Person("3", "Charlie", "charlie@mail.com", 50.0, "Berlin")]
        self.assertEqual(calculate_billing_average(single), 50.0)

    # --- process_csv_data ---
    def test_process_csv_data(self):
        input_data = [
            ("ID", "Name", "Email", "Billing", "Location"),
            ("1", "Alice", "alice@mail.com", "100.0", "Paris"),
            ("2", "", "bob@mail.com", "200.0", "London"),
            ("2", "Charlie", "charlie@mail.com", "150.0", "Madrid"),
            ("3", "Charlie", "charlie@mail.com", "150.0", "Berlin")
        ]
        result = process_csv_data(input_data)
        self.assertEqual(len(result), 3)

    def test_process_csv_data_missing_header_fields(self):
        input_data = [
            ("ID", "Name", "Email"),
            ("1", "Alice", "alice@mail.com")
        ]
        with self.assertRaises(ValueError):
            process_csv_data(input_data)
    
    def test_process_csv_data_empty(self):
        with self.assertRaises(ValueError):
            process_csv_data([])

    # --- mask_data ---
    def test_mask_data_output(self):
        people = [
            Person("1", "Alice Smith", "alice@mail.com", 100.0, "Paris"),
            Person("2", "Bob Stone", "bob@mail.com", 200.0, "London")
        ]
        avg = calculate_billing_average(people)
        masked = mask_data(people, avg)
        self.assertEqual(masked[0][1], "XXXXX XXXXX")
        self.assertEqual(masked[0][2], "XXXXX@XXXX.com")
        self.assertEqual(masked[0][3], 150.0)
    
    # --- read_file ---
    def test_read_file_reads_data(self):
        result = read_file("test.csv")
        self.assertEqual(result[0], ("ID", "Name", "Email", "Billing", "Location"))
        self.assertEqual(result[1], ("1", "John Doe", "john@example.com", "100.0", "New York"))

    
    # --- write_file ---
    def test_write_file_creates_file(self):
        data = [["1", "John", "john@mail.com", "100.0", "NY"]]
        write_file("test_write.csv", headers=["ID", "Name", "Email", "Billing", "Location"], data=data)
        self.assertTrue(os.path.exists("test_write.csv"))
        with open("test_write.csv") as f:
            content = f.read().strip().splitlines()
            self.assertEqual(content[0], "ID,Name,Email,Billing,Location")
            self.assertEqual(content[1], "1,John,john@mail.com,100.0,NY")

if __name__ == "__main__":
    unittest.main()