#test_railway

from pytest import raises, approx
import math
from pathlib import Path
import matplotlib.pyplot as plt
from utilities import read_rail_network
from railway import fare_price, Station, RailNetwork

# [Done] At least one test for the fare_price function (1 mark)

def test_fare_price(): 
   assert round(fare_price(1,0,0),2) == approx(1.99)

def test_fare_price_regions():
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

   assert station_1.distance_to(station_1) == 0.

# [Done] Tests for RailNetwork simple information functions (3 marks)

#set up a miscellaneous network with managable data: 6 stations, 3 regions, 2 hubs
abbey_wood = Station('Abbey Wood', 'London', 'ABW', 51.490719, 0.120343, 0)
aberdeen = Station('Aberdeen', 'Scotland','ABD', 57.143127, -2.097464, 1)
acton_central = Station('Acton Central', 'London', 'ACC', 57.143127, -2.097464, 0)
kirkcaldy = Station('Kirkcaldy','Scotland','KDY', 56.112579, -3.167445, 0)
kings_cross = Station('London Kings Cross', 'London', 'KGX',51.530827, -0.122907, 1)
ystrad_rhondda = Station('Ystrad Rhondda','Wales','YSR',51.644478,-3.47557, 0)

misc_network = RailNetwork([abbey_wood, aberdeen, acton_central, kirkcaldy, kings_cross, ystrad_rhondda])

def test_rail_regions():
   assert len(misc_network.regions()) == 3

def test_rail_station_number():
   assert misc_network.n_stations() == 6

# [Done] Tests for the hub_stations and closest_hub methods (4 marks)

def test_rail_hub_stations():
   assert len(misc_network.hub_stations()) == 2

def test_rail_hubs_wrong_region_type():
   with raises(TypeError, match='data type incorrect for region, expected str'):
      misc_network.hub_stations(2)

def test_rail_hubs_wrong_region():
   with raises(KeyError):
      misc_network.hub_stations('test')

def test_closest_hub():
   assert misc_network.closest_hub(kirkcaldy) == aberdeen #only 2 stations in Scotland so must be closest

def test_closest_hub_no_hubs():
   with raises(KeyError):
      misc_network.closest_hub(ystrad_rhondda) #no other stations in Wales, error is in hub_stations but also flagged here

def test_closest_hub_for_hub():
   assert misc_network.closest_hub(aberdeen) == aberdeen #closest hub to hub is itself
 
# [Done] Tests for the journey_planner and journey_fare methods (6 marks)

def test_journey_planner_type():
   with raises(TypeError, match='crs must be 3 letter string'):
      misc_network.journey_planner(1,2)

def test_journey_planner_crs_length():
   with raises(ValueError, match='crs must be 3 letter string'):
      misc_network.journey_planner('abcd','wxyz')

def test_journey_planner_2_legs():
   kirkcaldy_to_aberdeen = [kirkcaldy, aberdeen]
   assert kirkcaldy_to_aberdeen == misc_network.journey_planner(kirkcaldy.crs, aberdeen.crs)

def test_journey_planner_3_legs_hub_start():
   aberdeen_to_abbey_wood = [aberdeen, kings_cross, abbey_wood]
   assert aberdeen_to_abbey_wood == misc_network.journey_planner(aberdeen.crs, abbey_wood.crs)

def test_journey_planner_3_legs_hub_end():
   kirkcaldy_to_kings_cross = [kirkcaldy, aberdeen, kings_cross]
   assert kirkcaldy_to_kings_cross == misc_network.journey_planner(kirkcaldy.crs, kings_cross.crs)

def test_journey_planner_4_legs():
   kirkcaldy_to_abbey_wood = [kirkcaldy, aberdeen, kings_cross, abbey_wood]   
   assert kirkcaldy_to_abbey_wood == misc_network.journey_planner(kirkcaldy.crs, abbey_wood.crs)

#impossible journeys are already flagged earlier so no need to test here

def test_journey_fare_2_legs():
   fare_price_kircaldy_to_aberdeen = fare_price(kirkcaldy.distance_to(aberdeen), 0, 1)
   assert fare_price_kircaldy_to_aberdeen == approx(misc_network.journey_fare(kirkcaldy.crs, aberdeen.crs))

def test_journey_fare_3_legs_hub_start():
   fare_price_kings_cross_to_kirkcaldy = fare_price(kings_cross.distance_to(aberdeen),1,1)
   fare_price_kings_cross_to_kirkcaldy += fare_price(aberdeen.distance_to(kirkcaldy),0,1)
   assert fare_price_kings_cross_to_kirkcaldy == approx(misc_network.journey_fare(kings_cross.crs, kirkcaldy.crs))

def test_journey_fare_3_legs_hub_end():
   fare_price_acton_central_to_aberdeen = fare_price(acton_central.distance_to(kings_cross),0,1)
   fare_price_acton_central_to_aberdeen += fare_price(kings_cross.distance_to(aberdeen),1,1)
   assert fare_price_acton_central_to_aberdeen == approx(misc_network.journey_fare(acton_central.crs, aberdeen.crs))

def test_journey_fare_4_legs():
   fare_price_kirkcaldy_to_abbey_wood = fare_price(kirkcaldy.distance_to(aberdeen),0,1)
   fare_price_kirkcaldy_to_abbey_wood += fare_price(aberdeen.distance_to(kings_cross),1,1)
   fare_price_kirkcaldy_to_abbey_wood += fare_price(kings_cross.distance_to(abbey_wood),0,1)
   assert fare_price_kirkcaldy_to_abbey_wood == approx(misc_network.journey_fare(kirkcaldy.crs,abbey_wood.crs))


# [Done] Tests for the plot_fare_to method (2 marks)

def test_plot_fares_to_save_bool():
   with raises(TypeError, match='save must be bool'):
      misc_network.plot_fares_to('KGX', save=1)

def test_plot_fares_to_save():
   del misc_network.stations['YSR']  #to avoid Wales flagging the plot
   misc_network.plot_fares_to('KGX', save=True)
   assert Path(f"./Fare_prices_to_London_Kings_Cross.png").exists() == True

def test_plot_fares_to_other_args():
   fig, ax = plt.subplots(figsize=(5,5))
   misc_network.plot_fares_to('KGX', save=False, ec='red') #no error















