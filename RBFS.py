import math
from typing import Dict, List, Tuple, Optional, Set

class RBFS:
    def __init__(self, roadmap):
        self.roadmap = roadmap
        # Max recursion depth relative to the number of cities
        self.max_depth_fraction = 0.5  

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

    def findPath(self, start: str, goal: str) -> List[str]:
        def rbfs_rec(node: str, f_limit: float, g_score: Dict[str, float], path: List[str], depth: int) -> Tuple[Optional[List[str]], float]:
            print(f"Exploring node: {node} at depth {depth}, f_limit: {f_limit}")

            # check if the current city is goal city
            if node == goal:
                print(f"Goal {goal} found!")
                return path + [node], g_score[node]

            # handle max depth 
            if depth > len(self.roadmap.cities) * self.max_depth_fraction:
                print("Dynamic recursion depth limit reached.")
                return None, float('inf')

            successors = []
            for neighbor, cost in self.roadmap.roads[node]:

                # Check if node is already visited
                if neighbor in path:
                    continue  
                
                g_cost = g_score[node] + cost  # g(n)
                h_cost = self.haversine(neighbor, goal)  # h(n)
                f_cost = g_cost + h_cost  # f(n)

                print(f"Neighbor: {neighbor}, g(n): {g_cost}, h(n): {h_cost}, f(n): {f_cost}")

                successors.append((neighbor, g_cost, f_cost))

            if not successors:
                print(f"No successors for {node}")
                return None, float('inf')

            successors.sort(key=lambda x: x[2])  # Sort by f-cost

            while successors:
                best_node, best_g, best_f = successors[0]
                if best_f > f_limit:
                    print(f"Best node {best_node} exceeds f_limit with f(n): {best_f}")
                    return None, best_f

                alternative = successors[1][2] if len(successors) > 1 else float('inf')
                print(f"Recursing into best node: {best_node}, alternative f(n): {alternative}")

                g_score[best_node] = best_g
                result, new_f = rbfs_rec(best_node, min(f_limit, alternative), g_score, path + [node], depth + 1)

                if result is not None:
                    return result, new_f

                # Update the successor with the new f-cost if the path was not found
                successors[0] = (best_node, best_g, new_f)
                successors.sort(key=lambda x: x[2])  # Re-sort after update

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