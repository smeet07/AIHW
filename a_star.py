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
        priorityQ = []
        heapq.heappush(priorityQ, (0, start))
        came_from = {}
        g_n = {start: 0}
        f_n = {start: self.haversine(start, goal)}

        while priorityQ:
            current_f_n, current = heapq.heappop(priorityQ)
            self.steps.append((g_n.copy(), f_n.copy(), came_from.copy(), priorityQ.copy()))

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor, distance in self.roadmap.get_neighbors(current):
                tentative_g_n = g_n[current] + distance
                if neighbor not in g_n or tentative_g_n < g_n[neighbor]:
                    came_from[neighbor] = current
                    g_n[neighbor] = tentative_g_n
                    f_n[neighbor] = tentative_g_n + self.haversine(neighbor, goal)
                    heapq.heappush(priorityQ, (f_n[neighbor], neighbor))

        return None

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        total_path.reverse()
        return total_path
