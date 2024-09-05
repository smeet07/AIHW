import heapq

def uniform_cost_search(road_network, start, goal):
    priorityQ = []
    heapq.heappush(priorityQ, (0, start))
    originating_city = {}
    g_n = {start: 0}

    while priorityQ:
        curr_city_g_n, curr_city = heapq.heappop(priorityQ)

        if curr_city == goal:
            return reconstruct_path(originating_city, curr_city)

        for neighbor, distance in road_network.get_neighbors(curr_city):
            temp = g_n[curr_city] + distance
            if neighbor not in g_n or temp < g_n[neighbor]:
                originating_city[neighbor] = curr_city
                g_n[neighbor] = temp
                heapq.heappush(priorityQ, (temp, neighbor))

    return None

def reconstruct_path(originating_city, curr_city):
    final_path = [curr_city]
    while curr_city in originating_city:
        curr_city = originating_city[curr_city]
        final_path.append(curr_city)
    final_path.reverse()
    return final_path
