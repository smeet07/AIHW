import sys
import matplotlib.pyplot as plt
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

def plot_step(road_network, a_star, step):
    fig, ax = plt.subplots(figsize=(12, 8))  # Increase figure size (width, height)
    for city1, neighbors in road_network.roads.items():
        for city2, _ in neighbors:
            lat1, lon1 = road_network.cities[city1].latitude, road_network.cities[city1].longitude
            lat2, lon2 = road_network.cities[city2].latitude, road_network.cities[city2].longitude
            ax.plot([lon1, lon2], [lat1, lat2], 'gray', linewidth=0.5)  # Thin gray lines for roads

    g_score, f_score, came_from, open_set = a_star.steps[step]
    
    # Plot all cities as dots
    for city in road_network.cities.values():
        ax.plot(city.longitude, city.latitude, 'o', color='gray')
        ax.text(city.longitude, city.latitude, city.name, fontsize=9, ha='right')

    # Plot the path taken so far from the start city to the current city
    if step > 0:
        current_city = list(came_from.keys())[-1]
        path_so_far = [current_city]
        
        while current_city in came_from:
            previous_city = came_from[current_city]
            lat1, lon1 = road_network.cities[previous_city].latitude, road_network.cities[previous_city].longitude
            lat2, lon2 = road_network.cities[current_city].latitude, road_network.cities[current_city].longitude
            
            ax.plot([lon1, lon2], [lat1, lat2], 'r-', linewidth=2)  # Path in red
            
            # Print the road segment currently being undertaken
            print(f"Step {step}: Considering road from {previous_city} to {current_city}")
            
            current_city = previous_city
            path_so_far.append(current_city)
        
        path_so_far.reverse()

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Step {step}')
    plt.savefig(f'step_{step}.png')
    plt.close()

def plot_map(road_network, path):
    fig, ax = plt.subplots(figsize=(12, 8))
    for city1, neighbors in road_network.roads.items():
        for city2, _ in neighbors:
            lat1, lon1 = road_network.cities[city1].latitude, road_network.cities[city1].longitude
            lat2, lon2 = road_network.cities[city2].latitude, road_network.cities[city2].longitude
            ax.plot([lon1, lon2], [lat1, lat2], 'gray', linewidth=0.5)  # Thin gray lines for roads

    # Plot cities
    for city in road_network.cities.values():
        ax.plot(city.longitude, city.latitude, 'o', color='gray')
        ax.text(city.longitude, city.latitude, city.name, fontsize=9, ha='right')

    # Plot final path
    for i in range(len(path) - 1):
        city1 = path[i]
        city2 = path[i + 1]
        lat1, lon1 = road_network.cities[city1].latitude, road_network.cities[city1].longitude
        lat2, lon2 = road_network.cities[city2].latitude, road_network.cities[city2].longitude
        ax.plot([lon1, lon2], [lat1, lat2], 'r-', linewidth=2, label='Final Path')
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Final Path')
    plt.legend()
    plt.savefig('final_path.png')
    plt.show()

def main():
    if len(sys.argv) != 6:
        print("Usage: RunCities.py Cities.txt Roads.txt <ALG> <START> <GOAL>")
        return
    
    cities_file = sys.argv[1]
    roads_file = sys.argv[2]
    algorithm = sys.argv[3]
    start_city = sys.argv[4]
    goal_city = sys.argv[5]

    road_network = load_data(cities_file, roads_file)

    if algorithm == "A*":
        a_star = AStar(road_network)
        path = a_star.findPath(start_city, goal_city)
        for step in range(len(a_star.steps)):
            plot_step(road_network, a_star, step)
    elif algorithm == "UCS":
        path = uniform_cost_search(road_network, start_city, goal_city)
    elif algorithm == "RBFS":
        rbfs = RBFS(road_network)
        path = rbfs.findPath(start_city, goal_city)
    else:
        print("Unknown algorithm:", algorithm)
        return

    if path:
        print(f"Path found: {' -> '.join(path)}")
        plot_map(road_network, path)
    else:
        print("No path found.")

if __name__ == "__main__":
    main()
