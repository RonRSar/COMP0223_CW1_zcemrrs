import csv
from railway import Station, RailNetwork
from pathlib import Path

def read_rail_network(filepath):
    """
    A function to read CSV file of rail network and import them into the Station and RailNetwork classes.
    """
    assert isinstance(filepath, Path) , 'data type incorrect for filepath'

    reader = open(filepath, newline='')
    stations = csv.reader(reader, delimiter=',')

    stations_list = list(stations) #making into list as csv.reader is not iterable

    network_stations = []
    for row in stations_list[1:]: # 0th element is header
        CRS, Name, Coords_lat, Coords_long, Region, Hub = [cell for cell in zip(row)]
        network_stations.append(Station(name=Name, region=Region, crs=CRS, lat=Coords_lat, lon=Coords_long, hub=Hub))
        
    rail_network = RailNetwork(network_stations)

    return rail_network
