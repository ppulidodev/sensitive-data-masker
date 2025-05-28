import sys
import re
from person import Person
from typing import Union, List, Tuple, Dict

def read_file(file_path, delimiter=','):
    """
    Reads the content of a CSV file and return its content as a list of tuples.
    Each tuple contains the values of a row.
    """
    try:
        with open(file_path, 'r') as file:
            content = []

            text = file.read()
            for line in text.split('\n'):
                if line.strip():
                    items = line.split(delimiter)
                    content.append(tuple(items))

            return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def write_file(filename, headers= None, data= List[List], delimiter=','):
    """
    Writes data to a CSV file.
    If headers are provided, they will be written as the first row.
    The data should be a list of people where each Person represents a row.
    """
    try:
        with open(filename, 'w') as file:
            if headers:
                file.write(delimiter.join(headers) + '\n')
            for person in data:
                file.write(delimiter.join(str(x) for x in person) + '\n')
        print(f"CSV file '{filename}' has been written correctly.")
    except Exception as e:
        print(f"An unexpected error occurred while writing the file: {e}")
        sys.exit(1)


    
def mask_letters_clean(name):
    """
    Mask letters with 'X', remove leading/trailing spaces, and reduce multiple spaces to one.
    """
    name = re.sub(r'[a-zA-Z]', 'X', name)
    name = re.sub(r'\s+', ' ', name)
    return name.strip() 

def mask_email(email):
    """
    Masks the email by replacing all alphabet characters,
    except '@', before the first dot with 'X'.
    Assumes the email is already validated.
    """
    local, domain = email.split("@", 1)
    domain_parts = domain.split(".")

    masked_local = re.sub(r'[a-zA-Z]', 'X', local)
    masked_domain_first = re.sub(r'[a-zA-Z]', 'X', domain_parts[0])
    
    masked_email = f"{masked_local}@{masked_domain_first}"
    if len(domain_parts) > 1:
        masked_email += "." + ".".join(domain_parts[1:])
    
    return masked_email

def calculate_billing_average(candidates):
    """
    Calculates the average billing from a list of Person objects.
    Assumes each candidate has a 'billing' attribute as a float.
    Returns the average billing amount as a float.
    """
    total = sum(person.billing for person in candidates)
    count = len(candidates)
    return total / count if count > 0 else 0.0

def print_summary_report(candidates: List[Person]):
    """
    Prints a report with max, min, and average values for:
    - Name length (excluding spaces)
    - Billing amount
    """
    if not candidates:
        print("No valid candidates to report.")
        return

    name_lengths = [len(person.name.replace(" ", "")) for person in candidates]
    billings = [person.billing for person in candidates]

    name_max = max(name_lengths)
    name_min = min(name_lengths)
    name_avg = sum(name_lengths) / len(name_lengths)

    billing_max = max(billings)
    billing_min = min(billings)
    billing_avg = sum(billings) / len(billings)

    print("====================================================================================")
    print("Input data report:")
    print(f"Name:    Max. {name_max}, Min. {name_min}, Avg. {round(name_avg, 2)}")
    print(f"Billing: Max. {billing_max:.2f}, Min. {billing_min:.2f}, Avg. {billing_avg:.2f}")
    print("====================================================================================")


def process_csv_data(uncleaned_data: List[Union[List, Tuple, Dict]]):
    """
    Processes raw CSV data into a list of Person objects.
    Handles both list-based and dictionary-based row formats.
    Skips duplicate IDs and invalid rows, logging appropriate messages.
    """
    candidates = []
    seen_ids = set()

    if not uncleaned_data:
        raise ValueError("Input data is empty.")

    header = uncleaned_data[0]
    required_fields = ['ID', 'Name', 'Email', 'Billing', 'Location']

    
    if not all(field in header for field in required_fields):
        missing = [field for field in required_fields if field not in header]
        raise ValueError(f"Missing required fields in header: {missing}")

    data = uncleaned_data[1:]

    for i, row in enumerate(data):
        print(f"Started processing row {i + 1}")

        try:
            person_id = row[0]
            if person_id in seen_ids:
                print(f"Duplicate ID at row {i + 1}: {person_id}, skipping.")
                continue

            person = Person(
                _id=person_id,
                name= row[1],
                email= row[2],
                billing= row[3],
                location= row[4]
            )

            candidates.append(person)
            seen_ids.add(person_id)

        except Exception as e:
            print(f"Row {i + 1} is invalid: {e}")
            continue

    return candidates



def mask_data(data, average_billing):
    """
    Applies masking to the name, email, and location of each Person object.
    Returns a list of lists containing the masked data, ready to be written to a CSV file.
    """
    masked_rows = []
    for person in data:
        masked_row = [
            person.id,
            mask_letters_clean(person.name),
            mask_email(person.email),
            average_billing,
            mask_letters_clean(person.location)
        ]
        masked_rows.append(masked_row)
    return masked_rows

