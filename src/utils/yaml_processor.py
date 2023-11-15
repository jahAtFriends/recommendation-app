import yaml
import os

def read_yaml(file_path):
    """
    Function to read a YAML file and return a dictionary.
    """
    abs_file_path = os.path.join(os.getcwd(), 'data', file_path)
    with open(abs_file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def write_yaml(data, file_path):
    """
    Function to write a dictionary to a YAML file.
    """
    abs_file_path = os.path.join(os.getcwd(), 'data', file_path)
    with open(abs_file_path, 'w') as file:
        yaml.safe_dump(data, file)