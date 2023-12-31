import csv
import os

def read_csv(file_path):
    """
    Reads a CSV file and returns a list of dictionaries.
    Each dictionary represents a row in the CSV file.
    """
    abs_path = os.path.join(os.getcwd(), 'data', file_path)
    with open(abs_path, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(file_path, data, fieldnames):
    """
    Writes a list of dictionaries to a CSV file.
    Each dictionary in the list represents a row in the CSV file.
    """
    abs_path = os.path.join(os.getcwd(), 'output', file_path)
    with open(abs_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)