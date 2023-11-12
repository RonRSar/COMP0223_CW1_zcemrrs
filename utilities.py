import csv
from pathlib import Path

def read_rail_network(filepath):
    """
    A function to read CSV files and import them for use. 
    """
    assert isinstance(filepath, Path) , 'data type incorrect for filepath'

    reader = open(filepath, newline='')
    rail_network = csv.reader(reader, delimiter=';')
    return rail_network
