# sensitive-data-masker

This project focuses on processing a CSV file and masking any sensitive data it may contain.

## Features

- Read a `.csv` file with the structure: `[ID;Name;Email;Billing;Location]`
- Mask sensitive data:
  - **Name**: replace each letter with 'X', preserving the original length
  - **Email**: replace letters with 'X' while keeping the original length and top-level domain (e.g., `.com`)
  - **Billing**: replace each billing value with the overall average
  - **Location**: replace each letter with 'X', preserving the original length
- Write the masked data to a file named `masked_clients.csv`

## Assumptions

- Any row containing errors will be deemed invalid and excluded from processing.
- The expected input fields are: `ID`, `Name`, `Email`, `Billing`, and `Location`.

## Installation

Clone the repository:

```
git clone https://github.com/ppulidodev/sensitive-data-masker.git
cd sensitive-data-masker
```

## Requirements

- Python 3.8+

## Usage

From the project folder run 
```
python3 -m main.py /path-to-the-file
```

## Project Structure
```
sensitive-data-masker/
├── __init__.py 
├── main.py 
├── README.md 
├── person.py 
├── utils.py 
├── exceptions.py 
├── .gitignore 
├── data/ 
│   └── customer.csv
└── test/ 
    ├── __init__.py
    ├── test_person.py 
    └── tests_utils.py
```
## Testing

This project uses Python's built-in `unittest` module for testing.

To run all tests, execute the following command from the project root:

```
python3 -m unittest discover -s test
```

## Example

**Input:**
```
ID,Name,Email,Billing,Location
1,John Smith,john@mail.com,15000,New York
2,Kelly Lawrence Gomez,Kelly@your-mail.com,20000,Washington
3,Carl Winslow,carl-wins@mail-bot.com, ,Seattle
4,Roger Rogers,doubleR@mailer.com,12400.27,Boston
5,Gerald Frances, gf@jmail.com,53000,Dallas
```
**Output:**
```
ID,Name,Email,Billing,Location
1,XXXX XXXXX,XXXX@XXXX.com,25100.0675,XXX XXXX
2,XXXXX XXXXXXXX XXXXX,XXXXX@XXXX-XXXX.com,25100.0675,XXXXXXXXXX
4,XXXXX XXXXXX,XXXXXXX@XXXXXX.com,25100.0675,XXXXXX
5,XXXXXX XXXXXXX,XX@XXXXX.com,25100.0675,XXXXXX
```