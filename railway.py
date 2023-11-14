import matplotlib.pyplot as plt
import math 


def fare_price(distance, different_regions, hubs_in_dest_region):
    '''
    Function to calculate the fare_price based on the direct distance between stations, region and number of hubs in region
    '''
    fare_price = 1 + distance*math.exp(-distance/100)*(1+(different_regions*hubs_in_dest_region)/10)
    return fare_price


class Station:
    def __init__(self, name, region, crs, lat, lon, hub):
        self.name = name
        self.region = region                
        self.crs = crs
        self.lat = float(lat)
        self.lon = float(lon)
        self.hub = hub

        #Verify type
        assert isinstance(self.name, str), 'data type incorrect for Station name, expected str'
        assert isinstance(self.region, str), 'data type incorrect for Station region, expected str'
        assert isinstance(self.crs, str), 'data type incorrect for Station CRS, expected str'
        assert isinstance(self.lat, float), 'data type incorrect for Latitude, expected numeric'
        assert isinstance(self.lon, float), 'data type incorrect for Longitude, expected numeric'

        #Verify Correct values
        assert len(self.crs) == 3, 'CRS is incorrect length, expected 3 letters'
        assert -90 <= self.lat <= 90 , 'Latitude is not in -90 to 90 range'
        assert -180 <= self.lon <= 180, 'Longitude is not in -180 to 180 range'
        assert int(hub) == 0 or int(hub) == 1, 'input incorrect for hub, expected bool or 0/1' 
 

    def __str__(self):
        if int(self.hub) == 0:
            return f'Station({self.crs}-{self.name}/{self.region})'
        else:
            return f'Station({self.crs}-{self.name}/{self.region}-hub)'
        
    def __repr__(self): #same as __str__ 
        if int(self.hub) == 0:
            return f'Station({self.crs}-{self.name}/{self.region})'
        else:
            return f'Station({self.crs}-{self.name}/{self.region}-hub)'


    def distance_to(self, other_station):
        #splitting equation for easier readability and error checking
        lat_dif = (other_station.lat - self.lat)*0.5
        lon_dif = (other_station.lon - self.lon)*0.5

        #multiplying by pi/180 to convert from radian to degrees
        k_1 = math.sqrt((math.sin(lat_dif*math.pi/180))**2 + 
                        ((math.cos(self.lat*math.pi/180)*math.cos(other_station.lat*math.pi/180))*(math.sin(lon_dif*math.pi/180))**2))
        
        R = 6371 #declaring R as constant in case earth explodes and loses width
        distance = abs(2*R*math.asin(k_1)) #abs to prevent negative distances
        return distance


class RailNetwork:
    def __init__(self, stations):
        self.stations = stations #station input is list

        keys = [] #CRS are unique identifiers
        for row in range(int(len(self.stations))):
            keys.append(self.stations[row].crs)

        #ensure no duplicate CRS    
        assert len(keys) == len(set(keys)), 'There are duplicate CRS values, no stations can have the same identifier.'

        stations_dict = {}
        count = 0
        for station in self.stations:
            stations_dict[keys[count]] = station
            count += 1 #manually counting to prevent use of another loop structure

        #convert stations to dictionary
        self.stations = stations_dict


    def regions(self):
        '''
        Function finds the unique regions in a rail network
        '''
        region_list = []
        for key in self.stations.keys():
            region_list.append(str(self.stations[key].region))

        unique_regions = list(set(region_list)) #set finds unique regions in list
        return unique_regions

    def n_stations(self):
        '''
        Function counts number of stations in rail network
        '''
        n_stations = int(len(self.stations))
        return n_stations

    def hub_stations(self, region='all'):
        '''
        Function produces list of all hubmstations in rail network. 
        region can be set to specify an area, or left blank to return all hubs
        '''

        #verify region is string
        assert isinstance(region,str), 'data type incorrect for region, expected str'

        hub_stations = {}

        for key in self.stations.keys():
            if float(self.stations[key].hub) == 1: 
                hub_stations.setdefault(self.stations[key].region, []).append(self.stations[key])

        if region == 'all': #default value
            return hub_stations
        elif [region in self.regions()]:
            return hub_stations[region]
        else:
            raise KeyError('Region not in network') #case where region is inputted wrong or does not exist
        

    def closest_hub(self, s):
        '''
        Function takes a station and finds the closest hub to it in the same region.
        '''
        hubs_in_region = self.hub_stations(s.region)
        min = 1e7
        for station in hubs_in_region:
            dist = station.distance_to(s)
            if dist <= min: #if equidistant then goes alphabetical
                min = dist
                # if min == 0:
                #   continue #station is already hub, no need to codeify or flag since closest_hub is therefore station
                closest_hub = station
            elif min == 1e7:
                closest_hub = []
                print('No hub in region')

        return closest_hub

    
    def journey_planner(self, start, dest):
        '''
        Function takes the start and destination stations as crs inputs and returns a list of stations in the journey from start to end
        '''

        # find closest hub
        start_closest_hub = self.closest_hub(self.stations[start])
        end_closest_hub = self.closest_hub(self.stations[dest]) 

        journey = []
        journey.append(self.stations[start]) #start is always included

        #append if journey is inbetween regions
        if start_closest_hub != self.stations[start] and start_closest_hub.region != end_closest_hub.region:
            journey.append(start_closest_hub)
   
        if end_closest_hub != self.stations[dest] and end_closest_hub.region != start_closest_hub.region:
            journey.append(end_closest_hub)

        if self.stations[start] != self.stations[dest]:
            journey.append(self.stations[dest]) #end is included if start != end

        return journey
        

    def journey_fare(self, start, dest, summary=False):
        '''
        Function takes start and destination as crs values and returns the cost of the journey. 
        Summary is true to output more information and show the journey passage. 
        '''

        journey = self.journey_planner(start, dest)
        journey_fare = 0 #if 1 leg, then no cost

        if len(journey) == 2: # for simple 2 leg case
            distance = self.stations[start].distance_to(self.stations[dest])
            if self.stations[start].region == self.stations[dest].region:
                different_regions = 0
            else:
                different_regions = 1
            hubs_in_dest_region = len(self.hub_stations(self.stations[dest].region))
            journey_fare += fare_price(distance, different_regions, hubs_in_dest_region)

        if len(journey) >= 3: # for 3-4 leg case, selection structure instead of for loop for ease of visualisation
            distance = self.stations[start].distance_to(self.closest_hub(self.stations[start]))
            hubs_in_dest_region = len(self.hub_stations(self.closest_hub(self.stations[start]).region))
            journey_fare += fare_price(distance, 0, hubs_in_dest_region)

            if self.closest_hub(self.stations[start]).region == self.stations[dest].region: # 3 leg case- start/end xor hub 
                distance = self.closest_hub(self.stations[start]).distance_to(self.stations[dest])
                if self.closest_hub(self.stations[start]).region == self.stations[dest].region:
                    different_regions = 0
                else:
                    different_regions = 1
                hubs_in_dest_region = len(self.hub_stations(self.stations[dest].region))
                journey_fare += fare_price(distance, different_regions, hubs_in_dest_region)

            elif self.closest_hub(self.stations[start]).region != self.stations[dest].region: # 4 leg case- middle 2 are hubs
                distance = self.closest_hub(self.stations[start]).distance_to(self.closest_hub(self.stations[dest]))
                #dr is 1
                hubs_in_dest_region = len(self.hub_stations(self.stations[dest].region)) #hub in dest region is same region as dest
                journey_fare += fare_price(distance, 1, hubs_in_dest_region)
                distance = self.closest_hub(self.stations[dest]).distance_to(self.stations[dest])
                #dr is 0
                hubs_in_dest_region = len(self.hub_stations(self.stations[dest].region))
                journey_fare += fare_price(distance, 0, hubs_in_dest_region)
        



        if summary == True: 
            journey_disp = ""

            for i in range(len(journey)):
                if i == len(journey) - 1 or i == 0: #for start and dest
                    journey_disp += journey[i].crs
                else:
                    journey_disp += f'{journey[i].name} ({journey[i].crs})' #for expanding inbetween stations
                if i != len(journey) - 1: #for entering arrows 
                    journey_disp += ' -> '

            return f"Journey from: {self.stations[start].name} ({start}) to {self.stations[dest].name} ({dest})\n" f"Route: {journey_disp} \n" f"Fare: £{round(journey_fare, 2):.2f}"
        else:
            return journey_fare
        
        


    def plot_fares_to(self, crs_code, save, **args):
        """
        Function to plot all fares to one specific station. 
        Takes crs_code of station as input and produces histogram of fare prices from all other stations
        save is true for image to be saved locally to computer
        **args are used for the hist plot
        """
        fares = []
        for station in self.stations.values(): 
            if crs_code != station.crs: #ensure not checking self
                if [station.region in self.hub_stations()]: #ensure station can be travelled to
                    fares.append(self.journey_fare(station.crs, crs_code))
        
        station_name = self.stations[crs_code].name.replace(" ", "_")
        plt.title(f"Fare prices to {station_name}")
        plt.xlabel("Fare price (Pound)")

        if args != None: 
            plt.hist(fares, **args)
        else:
            plt.hist(fares)

        if save:
            plt.savefig(f"./Fare_prices_to_{station_name}.png")
        
        plt.waitforbuttonpress(0)

        
        return

    def plot_network(self, marker_size: int = 5) -> None:
        """
        A function to plot the rail network, for visualisation purposes.
        You can optionally pass a marker size (in pixels) for the plot to use.

        The method will produce a matplotlib figure showing the locations of the stations in the network, and
        attempt to use matplotlib.pyplot.show to display the figure.

        This function will not execute successfully until you have created the regions() function.
        You are NOT required to write tests nor documentation for this function.
        """
        fig, ax = plt.subplots(figsize=(5, 10))
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")
        ax.set_title("Railway Network")

        COLOURS = ["b", "r", "g", "c", "m", "y", "k"]
        MARKERS = [".", "o", "x", "*", "+"]

        for i, r in enumerate(self.regions()):
            lats = [s.lat for s in self.stations.values() if s.region == r]
            lons = [s.lon for s in self.stations.values() if s.region == r]

            colour = COLOURS[i % len(COLOURS)]
            marker = MARKERS[i % len(MARKERS)]
            ax.scatter(lons, lats, s=marker_size, c=colour, marker=marker, label=r)

        ax.legend()
        plt.tight_layout()
        plt.show()
        return

    def plot_journey(self, start: str, dest: str) -> None:
        """
        Plot the journey between the start and end stations, on top of the rail network map.
        The start and dest inputs should the strings corresponding to the CRS codes of the
        starting and destination stations, respectively.

        The method will overlay the route that your journey_planner method has found on the
        locations of the stations in your network, and draw lines to indicate the route.

        This function will not successfully execute until you have written the journey_planner method.
        You are NOT required to write tests nor documentation for this function.
        """
        # Plot railway network in the background
        network_lats = [s.lat for s in self.stations.values()]
        network_lons = [s.lon for s in self.stations.values()]

        fig, ax = plt.subplots(figsize=(5, 10))
        ax.scatter(network_lons, network_lats, s=1, c="blue", marker="x")
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")

        # Compute the journey
        journey = self.journey_planner(start, dest)
        plot_title = f"Journey from {journey[0].name} to {journey[-1].name}"
        ax.set_title(f"Journey from {journey[0].name} to {journey[-1].name}")

        # Draw over the network with the journey
        journey_lats = [s.lat for s in journey]
        journey_lons = [s.lon for s in journey]
        ax.plot(journey_lons, journey_lats, "ro-", markersize=2)

        plt.show()
        return
