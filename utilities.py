import csv
from railway import Station, RailNetwork
from pathlib import Path

def read_rail_network(filepath):
    """
    Function to read CSV file of a rail network and import them into the Station and RailNetwork classes.
    """
    assert isinstance(filepath, Path) , 'data type incorrect for filepath'

    reader = open(filepath, newline='')
    stations = csv.DictReader(reader, delimiter=',')

    network_stations = []
    for row in stations: 
        Name = row['name'] #assignment is based on csv headers, and not specific to csv format
        Region = row['region']
        CRS = row['crs']
        Coords_lat = float(row['latitude'])
        Coords_long = float(row['longitude'])
        Hub = row['hub']
        station = Station(Name, Region, CRS, Coords_lat, Coords_long, Hub)
        network_stations.append(station)
        
    rail_network = RailNetwork(network_stations)

    return rail_network
