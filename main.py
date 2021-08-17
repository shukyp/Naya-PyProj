# Python system Libs
import os
import networkx as nx
import matplotlib.pyplot as plt

# 3rd party Libs

# Appl modules
from json_io import *
from cMapCity import *
from cMap import *


# ---------------------------------------------------------------------------------------------------

# global definitions
DATA_PATH = './'
DFLT_NODE_COLOR = 'grey'
SLCT_NODE_COLOR = 'red'
DFLT_NODE_SIZE = 200
SLCT_NODE_SIZE = 700


# -------------------------------------------------------------------------------------------------
# load roads data. from file
# input:    fname - file to read
# returns:  roads info (structure)
def load_roads_info(fname):
    return json_load (fname)


# -------------------------------------------------------------------------------------------------
# assure road ID uniqueness
# input:    roads - roads group
# returns:  True-All IDs are unique, False - otherwise
def are_road_ids_unique(roads):

    # required to assure road's ID uniqueness
    road_ids = set ()

    # traverse thru all roads
    for road in roads:

        # extract road ID
        road_id = list (road.keys ())[0]

        #check if already encountered
        if (road_id in road_ids):
            return False                    # if not unique - quit
        road_ids.add (road_id)              # add to set

    # release memory
    del road_ids

    # advice caller
    return True


# -------------------------------------------------------------------------------------------------
# assure that every road has all the required attributes
# input:    roads - roads group
# returns:  True-All roads info is complete, False - otherwise
def is_road_info_complete(roads):

    for road in roads:
        road_attribs = list (road.values ())[0]
        road_attribs_names = road_attribs.keys ()
        #road_attribs_values = road_attribs.values ()

        # verify that all attribs (keys) are pesent
        road_attribs_list = list (road_attribs_names)  # dict keys
        if ((road_attribs_list.count ('city1') == 0) | (road_attribs_list.count ('city2') == 0) or
                (road_attribs_list.count ('distance') == 0) | (road_attribs_list.count ('status') == 0)):
            return False

    # advice caller
    return True


# -------------------------------------------------------------------------------------------------
# construct the road's attached cities, connect them, add them to the map
# input:    roads - roads group
#           map   - map of connected cities
# Returns:  None
def construct_cities_map(roads, map):

    # traverse thru all roads
    for road in roads:

        # get road's attributes  & values
        road_attribs = list (road.values ())[0]
        #road_attribs_names = road_attribs.keys ()
        #road_attribs_values = road_attribs.values ()

        # construct city1 object and add to map
        city_name = road_attribs['city1']
        city = MapCity(city_name)
        city.add_connected_city(road_attribs['city2'], road_attribs['distance'], road_attribs['status'])
        map.insert_city_to_map (city)

        # construct city2 object and add to map
        city_name = road_attribs['city2']
        city = MapCity(city_name)
        city.add_connected_city(road_attribs['city1'], road_attribs['distance'], road_attribs['status'])
        map.insert_city_to_map (city)


# -------------------------------------------------------------------------------------------------
# construct the road's attached cities, connect them, add them to the map
# input:    roads - roads group
#           route - set of cities selected to be the route
# Returns:  None
def visualize_route(roads, route=None):

    # show graph
    g = nx.Graph()

    edges_list = list()
    edges_set = set()
    edge_labels = dict()

    for road in roads:
        road_attribs = list (road.values ())[0]
        #road_attribs_names = road_attribs.keys ()
        road_attribs_values = list(road_attribs.values ())

        edge = (road_attribs['city1'], road_attribs['city2'])
        inverse_edge = (road_attribs['city2'], road_attribs['city1'])


        if (edge not in edges_set):
            edges_list.append(edge)
            edges_set.add(edge)
            edges_set.add(inverse_edge)
            edge_labels[edge] = road_attribs['distance']

    g.add_edges_from(edges_list)

    # set route nodes colors
    color_map = [DFLT_NODE_COLOR for node in g.nodes]
    if (route != None):
        for city_info in route:
            color_map[list(g.nodes).index(city_info[0])] = SLCT_NODE_COLOR

    # set route nodes size
    size_map = [DFLT_NODE_SIZE for ind in g.nodes]
    if (route != None):
        for city_info in route:
            size_map[list(g.nodes).index(city_info[0])] = SLCT_NODE_SIZE

    #pos = nx.spring_layout (g)

    # show the map
    nx.draw_networkx (g, node_color=color_map, node_size=size_map, with_labels=True)
    # nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_color='green', font_size=7)
    if (route != None):
        plt.title (f'Find a route between 2 cities {route[0][0]} - {route[-1][0]}')
    else:
        plt.title ('Map of cities')
    plt.show()


# ---------------------------------------------------------------------------------------------------
# manages the process of route search and visualization
# input:    roads - roads group
#           cities_map - set of cities that construct the cities map
#           start_city - the city where route starts
#           destination_city - the city where route terminates
# Returns:  None
def manage_route_search(roads, cities_map, start_city, destination_city):

    # search for a route in the map
    print(f'\n\nSearching a path from {start_city} to {destination_city} ...')
    cities_map.find_route (start_city, destination_city)

    # fetch & visualize the route
    route_len, route = cities_map.select_best_route (criteria='distance', show_routes=True)
    if (len (route) != 0):
        visualize_route (roads, route)
    else:
        print ('No route found')
    pass

# ---------------------------------------------------------------------------------------------------
def main():
    cities_map = Map ()
    roads = list ()

    # load road data
    roads = load_roads_info(DATA_PATH + 'roads.json')

    # assure road ID uniqueness
    ok = are_road_ids_unique(roads)
    if (not ok):
        print('\n\nnon-unique Roads ID found ... quit')
        exit(1)

    # assure road data completeness
    ok = is_road_info_complete (roads)
    if (not ok):
        print('\n\nRoad found to be incomplete ... quit')
        exit(1)

    # construct the map
    construct_cities_map(roads, cities_map)
    print('\n\nCities Map successfully constructed')

    # show map info
    print(cities_map)

    # visualize map
    visualize_route(roads)

    # find a route : 'City-A2' => 'City-C2'
    start_city = 'City-A2'; destination_city = 'City-C2'
    manage_route_search (roads, cities_map, start_city, destination_city)

   # find a route
    start_city = 'City-A1'; destination_city = 'City-C3'
    manage_route_search (roads, cities_map, start_city, destination_city)

    # Done
    print('We are done ... ')

# ---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print(os.getcwd()) #debug
    main()

