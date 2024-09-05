import math
from typing import Dict, List, Tuple, Optional

class AStar:
    def __init__(self, roadmap):
        self.roadmap = roadmap

    # Calculate haversine distance as heuristic
    def haversine(self, city1: str, city2: str) -> float:
        latitude1, longitude1 = self.roadmap.cities[city1].latitude, self.roadmap.cities[city1].longitude
        latitude2, longitude2 = self.roadmap.cities[city2].latitude, self.roadmap.cities[city2].longitude
        R = 6371  # Radius of Earth in km
        disatncelat = math.radians(latitude2 - latitude1)
        distancelon = math.radians(longitude2 - longitude1)
        # Calculate haversine distance
        distance = 2 * math.atan2(math.sqrt(math.sin(disatncelat / 2) ** 2 + math.cos(math.radians(latitude1)) * math.cos(math.radians(latitude2)) * math.sin(distancelon / 2) ** 2), math.sqrt(1 - math.sin(disatncelat / 2) ** 2 + math.cos(math.radians(latitude1)) * math.cos(math.radians(latitude2)) * math.sin(distancelon / 2) ** 2))
        # Return it multiplied by radius
        return R * distance

    def findPath(self, start: str, goal: str) -> List[str]:
        if start not in self.roadmap.cities or goal not in self.roadmap.cities:
            print(f"Either {start} or {goal} does not exist in the roadmap.")
            return []  # Return empty list if either city is missing

        priorityQ = {start}
        originating_city = {}
        g_n = {city: float('inf') for city in self.roadmap.cities}
        g_n[start] = 0
        f_n = {city: float('inf') for city in self.roadmap.cities}
        f_n[start] = self.haversine(start, goal)

        while priorityQ:
            current = min(priorityQ, key=lambda city: f_n[city])
            if current == goal:
                return self.reconstruct_path(originating_city, current)

            priorityQ.remove(current)
            for neighbor, cost in self.roadmap.get_neighbors(current):
                tentative_g_n = g_n[current] + cost
                if tentative_g_n < g_n[neighbor]:
                    originating_city[neighbor] = current
                    g_n[neighbor] = tentative_g_n
                    f_n[neighbor] = tentative_g_n + self.haversine(neighbor, goal)
                    if neighbor not in priorityQ:
                        priorityQ.add(neighbor)

        return []

    def reconstruct_path(self, originating_city: Dict[str, str], current: str) -> List[str]:
        path = [current]
        while current in originating_city:
            current = originating_city[current]
            path.append(current)
        path.reverse()
        return path
