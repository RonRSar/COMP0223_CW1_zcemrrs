import matplotlib.pyplot as plt


def fare_price(distance, different_regions, hubs_in_dest_region):
    raise NotImplementedError


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
        assert hub == 0 or hub == 1, 'input incorrect for hub, expected 0 or 1'        


    def distance_to(self):
        raise NotImplementedError


class RailNetwork:
    def __init__(self, stations):
        self.stations = stations

        keys = []
        for row in range(int(len(self.stations))):
            keys.append(self.stations[row].crs)
        assert len(keys) == len(set(keys)), 'There are duplicate CRS values, no stations can have the same identifier.'

        stations_dict = {}
        count = 0
        for station in self.stations:
            stations_dict[keys[count]] = station
            count += 1

        self.stations = stations_dict    


    def regions(self):
        region_list = []
        for k in range(int(len(self.stations))):
            region_list.append(str(self.stations[k].region))

        unique_regions = list(set(region_list))
        return unique_regions

    def n_stations(self):
        n_stations = int(len(self.stations))
        return n_stations

    def hub_stations(self, region):
        raise NotImplementedError

    def closest_hub(self, s):
        raise NotImplementedError

    def journey_planner(self, start, dest):
        raise NotImplementedError

    def journey_fare(self, start, dest, summary):
        raise NotImplementedError

    def plot_fares_to(self, crs_code, save, ADDITIONAL_ARGUMENTS):
        raise NotImplementedError

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

        for i, r in enumerate(self.regions):
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
