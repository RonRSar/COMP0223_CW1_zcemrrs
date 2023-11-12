import csv

def read_rail_network(filepath):
    """
    A function to read CSV files and import them for use. 
    """
    reader = open(filepath, newline='')
    rail_network = csv.reader(reader, delimiter=';')
    return rail_network
