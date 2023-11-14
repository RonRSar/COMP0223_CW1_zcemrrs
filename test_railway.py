#test_railway

from pytest import raises
from pathlib import Path
from utilities import read_rail_network
from railway import Station, RailNetwork

network_csv = Path("uk_stations.csv")
rail_network = read_rail_network(network_csv)


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



