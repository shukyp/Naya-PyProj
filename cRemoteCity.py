
#---------------------------------------------------------------------------------
# represents a remote connected city
# used by every city in the map in order to depict
# connection(roads) to other cities on the map
#---------------------------------------------------------------------------------
class RemoteCity(object):
    def __init__(self, city_name, distance, road_status):
        self.city_name = city_name
        self.distance = distance
        self.road_status = road_status

    def __str__(self):
        return f'city name: {self.city_name}, distance={self.distance}, status={self.road_status}'

    def get_road_distance(self):
        return (self.road_distance)

    def get_road_status(self):
        return (self.road_status)