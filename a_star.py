import heapq
import math
class AStar:
    def __init__(self, roadmap):
        self.roadmap = roadmap
        self.steps = []

    # calculate haversine distance as G score
    def haversine(self, city1: str, city2: str) -> float:
        # get the latitude and longitude from the text file
        latitude1, longitude1 = self.roadmap.cities[city1].latitude, self.roadmap.cities[city1].longitude
        latitude2, longitude2 = self.roadmap.cities[city2].latitude, self.roadmap.cities[city2].longitude
        R = 6371  # Radius of Earth in km
        disatncelat = math.radians(latitude2 - latitude1)
        distancelon = math.radians(longitude2 - longitude1)
        # calculate haversine distance
        distance = 2 * math.atan2(math.sqrt(math.sin(disatncelat / 2) ** 2 + math.cos(math.radians(latitude1)) * math.cos(math.radians(latitude2)) * math.sin(distancelon / 2) ** 2), math.sqrt(1 - math.sin(disatncelat / 2) ** 2 + math.cos(math.radians(latitude1)) * math.cos(math.radians(latitude2)) * math.sin(distancelon / 2) ** 2))
        # return it multiplied by radius
        return R * distance

    def findPath(self, start, goal):
        # priority queue to maintain the next city to consider
        priorityQ = []
        heapq.heappush(priorityQ, (0, start))
        originating_city = {}
        # intilialize g(n), f(n)
        g_n = {start: 0}
        f_n = {start: self.haversine(start, goal)}

        while priorityQ:
            current_f_n, current = heapq.heappop(priorityQ)
            self.steps.append((g_n.copy(), f_n.copy(), originating_city.copy(), priorityQ.copy()))

            # check if the current city is the goal
            if current == goal:
                return self.reconstruct_path(originating_city, current)

            # go through neighbors
            for next_city, distance in self.roadmap.get_next_citys(current):
                tentative_g_n = g_n[current] + distance
                if next_city not in g_n or tentative_g_n < g_n[next_city]:
                    originating_city[next_city] = current
                    # calculate g(n)
                    g_n[next_city] = tentative_g_n
                    # calculate f(n)
                    f_n[next_city] = tentative_g_n + self.haversine(next_city, goal)
                    heapq.heappush(priorityQ, (f_n[next_city], next_city))

        return None

    # print the final path output
    def reconstruct_path(self, originating_city, current):
        final_path = [current]
        while current in originating_city:
            current = originating_city[current]
            final_path.append(current)
        final_path.reverse()
        return final_path
