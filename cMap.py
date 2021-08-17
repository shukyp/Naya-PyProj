# a map is a dictionary of {'city-name':  [remote city-obj (reference)]}

class Map (object):

    def __init__(self):
        self.map_cities = dict()  # of remote cities
        self._routes_of_search = list()

    # --------------------------------------------------
    def insert_city_to_map(self, city_obj):

        # extract name of the city to be processed
        city_name = city_obj.city_name

        # if city isn't already part of the map
        if (city_name not in self.map_cities.keys()):
            self.map_cities[city_name] = [city_obj.remote_cities[0]]
            return

        # city is already in map. update its remote cities
        self.map_cities[city_name].append(city_obj.remote_cities[0])

    # --------------------------------------------------
    def get_route(self):
        return self._routes_of_search

    # --------------------------------------------------
    def find_route(self, start_city, destination_city):

        # init
        self._routes_of_search = list()             # reset search results
        map_cities = set(self.map_cities.keys())    # extract cities of the map
        otg_route = list()  # otg - on the go       # reset OTG route

        # assure both cities are part of the map
        if ((start_city not in map_cities) | (destination_city not in map_cities)):
            return

        # add start city to route
        otg_route.append((start_city, 0))  # add current city to route

        if (start_city == destination_city):
            otg_route.append(destination_city)  # add current city to route
            return

        # debug
        print(f'[Launch point] OTG route: {otg_route}')

        # launch recursive search
        self.__search_route(start_city, destination_city, otg_route)

    # --------------------------------------------------
    # recursive method
    def __search_route(self, curr_city, destination_city, otg_route):

        # stop conditions: route found, destination city reached
        if (curr_city == destination_city):
            self.__keep_route(otg_route)
            print(f'[ROUTE FOUND] OTG route: {otg_route}')  # debug
            otg_route.pop(-1)
            print(f'OTG route: {otg_route}')  # debug
            return

        # point to remote cities
        remote_cities = self.map_cities[curr_city]

        # dive recursively, avoid loops
        for remote_city in remote_cities:

            # extract remote city name
            remote_city_name = remote_city.city_name
            remote_city_distance = remote_city.distance
            print(f'Considering to visit {remote_city_name}')  # debug

            # avoid moving in circles - don't visit a city already visited
            if ([city for city, distance in otg_route].count(remote_city_name) != 0):
                continue

            # add remote city to route before moving to visit it
            # keep remotes city name and distance to it
            otg_route.append((remote_city_name, remote_city_distance))
            print(f'OTG route: {otg_route}')  # debug

            # recursive dive
            self.__search_route(remote_city_name, destination_city, otg_route)

        # drop current city from the route
        otg_route.pop(-1)
        print(f'OTG route: {otg_route}')  # debug

    # --------------------------------------------------
    def __keep_route(self, route):
        self._routes_of_search.append(route.copy())

    # --------------------------------------------------
    def select_best_route(self, criteria, show_routes):
        if (criteria == 'distance'):
            return self._select_best_route_by_distance(show_routes)

    # --------------------------------------------------
    def _select_best_route_by_distance(self, show_routes):
        # go thru each located route and calculate its length
        # prefer the best route

        # reset route counter
        route_cntr = 1

        # traverse thru all routes found during the route search
        # sum and keep each route length
        for route in self._routes_of_search:

            # reset route_len
            route_len = 0

            # traverse thru all route's cities
            # sum the distance between the cities of the route
            for city in route:
                route_len = route_len + city[1]

            if (show_routes):
                print(f'route #{route_cntr}: {route}, length={route_len}')
                route_cntr += 1

            # keep the route length
            route.insert(0, route_len)

        # select the the best route by distance
        route_len = -1  # used to find the shortest route
        route_cntr = 0  # points to selected route

        # traverse thru all routes, find the preferred (shortest( route
        for indx, route in enumerate(self._routes_of_search):

            if (route_len == -1):
                route_len = route[0]
                route_cntr = indx
                continue

            if (route[0] < route_len):
                route_len = route[0]
                route_cntr = indx
                continue

        if (show_routes):
            print(f'Preferred route #{route_cntr+1}, len:{route_len}, {self._routes_of_search[route_cntr][1:]}')

        route_len = self._routes_of_search[route_cntr][0]
        route = self._routes_of_search[route_cntr][1:]

        cities = [x[0] for x in route]
        distances = [x[1] for x in route]
        distances.pop(0); distances.append(0)
        route = [x for x in zip(cities, distances)]

        return (route_len, route)

    # --------------------------------------------------
    def __str__(self):
        map_str = ''
        for key in self.map_cities.keys():
            city_str = str(key)
            remote_cities_str = ''
            for remote_city in self.map_cities[key]:
                remote_cities_str = remote_cities_str + '\n' + str(remote_city)

            map_str = map_str + '\n\n' + city_str + '\t\t' + remote_cities_str

        return map_str
