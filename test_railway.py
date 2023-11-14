#test_railway

from pytest import raises, approx
import math
from pathlib import Path
from utilities import read_rail_network
from railway import fare_price, Station, RailNetwork

# [Done] At least one test for the fare_price function (1 mark)

def test_fare_price(): 
   assert round(fare_price(1,0,0),2) == approx(1.99)
   with raises(AssertionError, match = 'Different Regions must be 0 or 1'): #check diff regions is 1 or 0 only
     fare_price(1,2,3)

# [Done] At least four negative tests, checking the handling of improper inputs to Station (4 marks)

def test_station_name_type():
    with raises(TypeError, match = 'data type incorrect for Station name, expected str'): #check Station name is str
       Station(1,'b','abc',0.,0.,0)

def test_station_region_type():
    with raises(TypeError, match = 'data type incorrect for Station region, expected str'): #check Station region is str
       Station('a',2,'abc',0.,0.,0)

def test_station_crs_type():
    with raises(TypeError, match = 'data type incorrect for Station CRS, expected str'): #check Station CRS is str
       Station('a','b',123,0.,0.,0)

def test_station_lat_lon_type():
    with raises(TypeError, match='data type incorrect for Latitude, expected numeric'): #check lat is numeric
       Station('a','b','abc','x',0.,0)
    with raises(TypeError, match='data type incorrect for Longitude, expected numeric'): #check lon is numeric
       Station('a','b','abc',lat=0., lon='err',hub=0)

def test_station_crs_length():
    with raises(AssertionError, match= "CRS is incorrect length, expected 3 letters"): #check crs is 3 letters
     Station('a','b','c',0.,0.,0)

def test_station_lat_lon_values():
    with raises(ValueError, match='Latitude is not in -90 to 90 range'): #check lat range
       Station('a','b','abc',-91.,0.,0)
       Station('a','b','abc',91.,0.,0)
    with raises(ValueError, match='Longitude is not in -180 to 180 range'): #check lon range
       Station('a','b','abc',0.,-181.,0)
       Station('a','b','abc',0.,181.,0)

def test_station_hub():
    with raises(AssertionError, match='input incorrect for hub, expected bool or 0/1' ): #check hub
        Station('a','b','abc',0.,0.,-2)
        Station('a','b','abc',0.,0.,53)

# [Done] A test to check that CRS codes loaded into a RailNetwork are unique (1 mark)

def test_crs_unique():
   station_1 = Station('a','b','abc',0.,0.,0)
   station_2 = Station('x','y','abc',0.,0.,0)
   with raises(KeyError, match='There are duplicate CRS values, no stations can have the same identifier.'):
    RailNetwork([station_1,station_2])

# [Done] Test Station class distance_to method (2 marks)

def test_distance_to():
   station_1 = Station('a','b','abc',10.,-10.,0)
   station_2 = Station('x','y','xyz',-20.,15.,0)

   lat_dif = (station_1.lat-station_2.lat)*0.5
   lon_dif = (station_1.lon-station_2.lon)*0.5
   
   dist_1_to_2 = abs(2*6371*math.asin(math.sqrt((math.sin(lat_dif*math.pi/180))**2 + 
                    ((math.cos(station_1.lat*math.pi/180)*math.cos(station_2.lat*math.pi/180))*(math.sin(lon_dif*math.pi/180))**2))))
   
   assert dist_1_to_2 == approx(station_1.distance_to(station_2))

def test_distance_to_duplicate():
   station_1 = Station('a','b','abc',1.,-1.,0)
   station_2 = Station('x','y','xyz',1.,-1.,0)

   assert station_1.distance_to(station_2) == 0.

# ∘ Tests for RailNetwork simple information functions (3 marks)
abbey_wood = Station('Abbey Wood', 'London', 'ABW', 51.490719, 0.120343, 0)
aberdeen = Station('Aberdeen', 'Scotland','ABD', 57.143127, -2.097464, 1)
acton_central = Station('Acton Central', 'London', 'ACC', 57.143127, -2.097464, 0)
kirkcaldy = Station('Kirkcaldy','Scotland','KDY', 56.112579, -3.167445, 0)
kings_cross = Station('London Kings Cross', 'London', 'KGX',51.530827, -0.122907, 1)

misc_network = RailNetwork([abbey_wood, aberdeen, acton_central, kirkcaldy, kings_cross])

def test_rail_regions():
   assert len(misc_network.regions()) == 2

def test_rail_station_number():
   assert misc_network.n_stations() == 5

# ∘ Tests for the hub_stations and closest_hub methods (4 marks)


# ∘ Tests for the journey_planner and journey_fare methods (6 marks)


# ∘ Tests for the plot_fare_to method (2 marks)














