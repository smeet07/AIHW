import unittest
from a_star import AStar
from ucs import uniform_cost_search
from RBFS import RBFS
class City:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

class RoadMap:
    def __init__(self):
        self.cities = {}
        self.roads = {}

    def add_city(self, name, latitude, longitude):
        self.cities[name] = City(name, latitude, longitude)

    def append_road(self, city1, city2, distance):
        if city1 not in self.roads:
            self.roads[city1] = []
        if city2 not in self.roads:
            self.roads[city2] = []
        self.roads[city1].append((city2, distance))
        self.roads[city2].append((city1, distance))  # Bidirectional roads

    def get_neighbors(self, city):
        return self.roads.get(city, [])

def load_data(cities_file, roads_file):
    road_network = RoadMap()

    with open(cities_file, 'r') as file:
        for line in file:
            name, lat, lon = line.strip().split(',')
            road_network.add_city(name.strip(), float(lat), float(lon))

    with open(roads_file, 'r') as file:
        for line in file:
            city1, city2, distance = line.strip().split(',')
            road_network.append_road(city1.strip(), city2.strip(), float(distance))

    return road_network

class TestPathfindingAlgorithms(unittest.TestCase):
    def setUp(self):
        self.road_network = load_data('Cities.txt', 'Roads.txt')

    def test_ucs_short_path(self):
        path = uniform_cost_search(self.road_network, 'cleveland', 'wichita')
        expected = ['cleveland', 'dayton', 'indianapolis', 'kansasCity', 'wichita']
        self.assertEqual(path, expected)

    def test_astar_short_path(self):
        """Test A* for a simple short path."""
        a_star = AStar(self.road_network)
        result = a_star.findPath('washington', 'kansasCity')
        expected = ['washington', 'philadelphia', 'cleveland', 'dayton', 'indianapolis','kansasCity']
        self.assertEqual(result, expected)

    def test_ucs_long_path(self):
        """Test UCS for a more complex long path."""
        result = uniform_cost_search(self.road_network, 'newYork', 'sanFrancisco')  # Call as function
        expected = ['newYork', 'philadelphia', 'cleveland', 'dayton', 'indianapolis', 'kansasCity', 'wichita', 'denver', 'santaFe', 'elPaso', 'tucson', 'phoenix', 'sanDiego', 'losAngeles', 'sanLuisObispo', 'sanJose', 'sanFrancisco']
        self.assertEqual(result, expected)

    def test_rbfs_short_path(self):
        """Test RBFS for a simple short path."""
        rbfs = RBFS(self.road_network)
        result = rbfs.findPath('cleveland', 'wichita')
        expected = ['cleveland', 'dayton', 'indianapolis', 'kansasCity', 'wichita']
        self.assertEqual(result, expected)

    def test_rbfs_long_path(self):
        rbfs = RBFS(self.road_network)
        result = rbfs.findPath('japan', 'uk')
        expected = ['japan', 'sanLuisObispo', 'losAngeles', 'sanDiego', 'phoenix', 'tucson', 'elPaso', 'santaFe', 'denver', 'wichita', 'kansasCity', 'indianapolis', 'dayton', 'cleveland', 'philadelphia', 'uk']
        self.assertEqual(result, expected)

    def test_astar_long_path(self):
        a_star = AStar(self.road_network)
        result = a_star.findPath('keyWest', 'calgary')
        expected = ['keyWest', 'tampa', 'lakeCity', 'tallahassee', 'atlanta','memphis','tulsa', 'kansasCity', 'wichita', 'omaha', 'desMoines','minneapolis','winnipeg','calgary']
        self.assertEqual(result, expected)

    def test_astar_nonexistent_path(self):
        """Test A* for a path that doesn't exist (invalid city names)."""
        a_star = AStar(self.road_network)
        result = a_star.findPath('fakeCity1', 'fakeCity2')
        self.assertEqual(result, [])

    def test_ucs_nonexistent_path(self):
        """Test UCS for a path that doesn't exist (invalid city names)."""
        result = uniform_cost_search(self.road_network, 'fakeCity1', 'fakeCity2')
        self.assertEqual(result, [])

    def test_rbfs_nonexistent_path(self):
        """Test RBFS for a path that doesn't exist (invalid city names)."""
        rbfs = RBFS(self.road_network)
        result = rbfs.findPath('fakeCity1', 'fakeCity2')
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
