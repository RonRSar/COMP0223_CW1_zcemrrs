#test_railway

from pytest import raises
from pathlib import Path
from utilities import read_rail_network
from railway import Station, RailNetwork

network_csv = Path("uk_stations.csv")
rail_network = read_rail_network(network_csv)

def test_station():
    with raises(TypeError, match = 'data type incorrect for Station name, expected str'): #check Station name is str
       Station(1,'b','abc',0.,0.,0)
    with raises(TypeError, match = 'data type incorrect for Station region, expected str'): #check Station region is str
       Station('a',2,'abc',0.,0.,0)
    with raises(TypeError, match = 'data type incorrect for Station CRS, expected str'): #check Station CRS is str
       Station('a','b',123,0.,0.,0)
    with raises(TypeError, match='data type incorrect for Latitude, expected numeric'): #check lat is numeric
       Station('a','b','abc','x',0.,0)
    with raises(TypeError, match='data type incorrect for Longitude, expected numeric'): #check lon is numeric
       Station('a','b','abc',lat=0., lon='err',hub=0)

    with raises(AssertionError, match= "CRS is incorrect length, expected 3 letters"): #check crs is 3 letters
     Station('a','b','c',0.,0.,0)
    with raises(ValueError, match='Latitude is not in -90 to 90 range'): #check lat range
       Station('a','b','abc',-91.,0.,0)
       Station('a','b','abc',91.,0.,0)
    with raises(ValueError, match='Longitude is not in -180 to 180 range'): #check lon range
       Station('a','b','abc',0.,-181.,0)
       Station('a','b','abc',0.,181.,0)
    with raises(AssertionError, match='input incorrect for hub, expected bool or 0/1' ): #check hub
        Station('a','b','abc',0.,0.,-2)
        Station('a','b','abc',0.,0.,53)

        


#call pytest from bash terminal
#pytest functions have to have test in them. 

# From assignment
# Errors with appropriate error messages are thrown when invalid values are encountered (see Reading
# and validating data section above)
# • The Station methods work correctly
# • For the RailNetwork class:
# ∘ The methods and properties providing simple information about the collection work correctly.
# ∘ The hub_stations and closest_hub methods work as intended, in the case of
# hub_stations including the case when it is passed optional arguments.
# ∘ journey_planner correctly determines the journeys to be taken between stations.
# ∘ journey_fare correctly determines the fare prices for journeys of different numbers of legs.

# • Tests (23%)
# ∘ At least one test for the fare_price function (1 mark)
# ∘ At least four negative tests, checking the handling of improper inputs to Station (4 marks)
# ∘ A test to check that CRS codes loaded into a RailNetwork are unique (1 mark)
# ∘ Test Station class distance_to method (2 marks)
# ∘ Tests for RailNetwork simple information functions (3 marks)
# ∘ Tests for the hub_stations and closest_hub methods (4 marks)
# ∘ Tests for the journey_planner and journey_fare methods (6 marks)
# ∘ Tests for the plot_fare_to method (2 marks)



