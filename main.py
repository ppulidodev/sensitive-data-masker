import argparse
from utils import (
    read_file, write_file, calculate_billing_average,
    process_csv_data, print_summary_report, mask_data
)


def main():
    parser = argparse.ArgumentParser(
        description="Process and mask sensitive client data from a CSV file."
    )
    parser.add_argument(
        "input_file",
        help="Path to the input CSV file."
    )
    parser.add_argument(
        "-o", "--output_file",
        default="data/masked_clients.csv",
        help="Path to save the masked output CSV file (default: data/masked_clients.csv)"
    )

    args = parser.parse_args()

    try:
        uncleaned_data = read_file(args.input_file)
        cleaned_data = process_csv_data(uncleaned_data)
        average_billing = calculate_billing_average(cleaned_data)
        masked_data = mask_data(cleaned_data, average_billing)
        write_file(args.output_file, headers=["ID", "Name", "Email", "Billing", "Location"], data=masked_data)
        
        print_summary_report(cleaned_data)
        print(f"Masked data written to {args.output_file}")
        
    except Exception as e:
        print(f"Error processing CSV: {e}")
        raise

if __name__ == "__main__":
    main()