import csv
from railway import Station, RailNetwork
from pathlib import Path

def read_rail_network(filepath):
    """
    Function to read CSV file of a rail network and import them into the Station and RailNetwork classes.
    """
    assert isinstance(filepath, Path) , 'data type incorrect for filepath'

    reader = open(filepath, newline='')
    stations = csv.reader(reader, delimiter=',')

    stations_list = list(stations) #making into list as csv.reader is not iterable

    network_stations = []
    for row in stations_list[1:]: # 0th element is header
        CRS, Name, Coords_lat, Coords_long, Region, Hub = [cell for cell in zip(row)] #To Do: Generalise
        
        #converting from tuple
        CRS = str(CRS)
        Name = str(Name)
        Coords_lat = str(Coords_lat)
        Coords_long = str(Coords_long)
        Region = str(Region)
        Hub = str(Hub)

        #stripping extra information
        network_stations.append(Station(name=Name.strip('\'(\',)'), region=Region.strip('\'(\',)'), crs=CRS.strip('\'(\',)'),
                                        lat=float(Coords_lat.strip('\'(\',)')), lon=float(Coords_long.strip('\'(\',)')), 
                                        hub=bool(Hub.strip('\'(\',)'))))
        
    rail_network = RailNetwork(network_stations)

    return rail_network
