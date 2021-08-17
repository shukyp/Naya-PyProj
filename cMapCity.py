
from cRemoteCity import *

#---------------------------------------------------------------------------------
# represents a city on the map
#---------------------------------------------------------------------------------
class MapCity(object):

    def __init__(self, city_name):
        self.city_name = city_name
        self.remote_cities = list()

    def __str__(self):
        connected_cities_str  = ''
        for remote_city in self.remote_cities:
            connected_cities_str =  connected_cities_str  +  ' \n\t\t ' +  str(remote_city)
        return f'\n\tcity name: {self.city_name}, \n\tconnected cities = {connected_cities_str}'

    def add_connected_city(self, city_name, distance, road_status):
        remote_city = RemoteCity(city_name, distance, road_status)
        self.remote_cities.append(remote_city)
