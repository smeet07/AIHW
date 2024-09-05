import math
from typing import Dict, List, Tuple, Optional

class RBFS:
    def __init__(self, roadmap):
        self.roadmap = roadmap
        # Max recursion depth relative to the number of cities
        self.max_depth_fraction = 0.5  

    # Calculate haversine distance as G score
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
        if start not in self.roadmap.roads or goal not in self.roadmap.roads:
            print(f"Either {start} or {goal} does not exist in the roadmap.")
            return []  # Return empty list if either city is missing

        def rbfs_rec(node: str, f_limit: float, g_score: Dict[str, float], path: List[str], depth: int) -> Tuple[Optional[List[str]], float]:
            # Check if the current city is goal city
            if node == goal:
                print(f"City {goal} Reached, Hurayyyyy")
                return path + [node], g_score[node]

            # Handle max depth 
            if depth > len(self.roadmap.cities) * self.max_depth_fraction:
                print("Dynamic recursion depth limit reached.")
                return None, float('inf')

            priorityQ = []

            # Go through all neighboring cities
            for next_city, cost in self.roadmap.roads.get(node, []):
                # Check if node is already visited
                if next_city in path:
                    continue  
                
                g_n = g_score[node] + cost  # g(n)
                h_n = self.haversine(next_city, goal)  # h(n)
                f_n = g_n + h_n  # f(n)

                print(f"Neighbor city: {next_city}, g(n): {g_n}, h(n): {h_n}, f(n): {f_n}")
                # Add to priority queue
                priorityQ.append((next_city, g_n, f_n))

            # Return inf if no further nodes
            if not priorityQ:
                print(f"No priorityQ for {node}")
                return None, float('inf')

            # Sort the list to make it a priorityQueue
            priorityQ.sort(key=lambda x: x[2])  # Sort by f-cost

            while priorityQ:
                best_node, best_g, best_f = priorityQ[0]
                # Backtrack if f-score is more than f limit
                if best_f > f_limit:
                    print(f"Best node {best_node} exceeds f_limit with f(n): {best_f}")
                    return None, best_f

                # Get the next best f score
                alternative = priorityQ[1][2] if len(priorityQ) > 1 else float('inf')
                print(f"Recursing into best node: {best_node}, alternative f(n): {alternative}")

                g_score[best_node] = best_g
                # Update f limits
                result, new_f = rbfs_rec(best_node, min(f_limit, alternative), g_score, path + [node], depth + 1)

                if result is not None:
                    return result, new_f

                # Update the successor with the new f-cost if the path was not found
                priorityQ[0] = (best_node, best_g, new_f)
                # Re-sort after update
                priorityQ.sort(key=lambda x: x[2])

            return None, float('inf')

        # Initialize g(n) for the start node
        g_score = {start: 0}

        print(f"Starting RBFS search from {start} to {goal}")
        path, _ = rbfs_rec(start, float('inf'), g_score, [], 0)

        if path:
            print(f"Path found: {' -> '.join(path)}")
            return path
        else:
            print("No path found")
            return []
