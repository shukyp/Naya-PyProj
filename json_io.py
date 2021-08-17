
import json


# ---------------------------------------------------------------------------------------------------
# serializes a python object to JSON format (text) file
# Input     fname   - file name to write
#           obj     - python structure (data object)
def json_dump(fname, obj):
    try:
        with (open(fname, 'w')) as f:
            f.write(json.dumps(obj, indent=2))
            f.close();
    except:
        print(f'[{json_dump.__name__}]Failed to create {fname}')


# ---------------------------------------------------------------------------------------------------
# deserialize a JSON format (text) file to a python structure
# Input:    fname - file to read
# Output:   python structure (data object)
def json_load(fname):
    try:
        with (open(fname, 'r')) as f:
            json_str = f.read()
            f.close();
            return json.loads(json_str)
    except:
        print(f'[{json_load.__name__}] Failed to open {fname}')

# ---------------------------------------------------------------------------------------------------
# construct_roads_json_file (DATA_PATH + 'roads.json')
def construct_roads_json_file(fname):
    # construct roads JSON file
    roads = [
        {1: {'city1': 'City-A1', 'city2': 'City-A2', 'distance': 15.2, 'status': 1}},
        {2: {'city1': 'City-A2', 'city2': 'City-A3', 'distance': 7.7, 'status': 1}},
        {3: {'city1': 'City-A2', 'city2': 'City-B2', 'distance': 4.5, 'status': 1}},
        {4: {'city1': 'City-A2', 'city2': 'City-B1', 'distance': 5.6, 'status': 1}},
        {5: {'city1': 'City-B1', 'city2': 'City-C2', 'distance': 13.9, 'status': 1}},
        {6: {'city1': 'City-B2', 'city2': 'City-C2', 'distance': 9.7, 'status': 1}},
        {7: {'city1': 'City-C1', 'city2': 'City-C2', 'distance': 6.3, 'status': 1}},
        {8: {'city1': 'City-C2', 'city2': 'City-C3', 'distance': 23.4, 'status': 1}}
    ]

    json_dump (fname, roads)
