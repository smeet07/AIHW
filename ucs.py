import heapq

def uniform_cost_search(road_network, start, goal):
    # maintain queue to keep track of the cities and g(n) values
    priorityQ = []
    heapq.heappush(priorityQ, (0, start))
    originating_city = {}
    g_n = {start: 0}

    while priorityQ:
        # pop the g(n) and the city from queue
        curr_city_g_n, curr_city = heapq.heappop(priorityQ)
        # check if city is the goal
        if curr_city == goal:
            return reconstruct_path(originating_city, curr_city)
        # go through neighboring cities
        for neighbor, distance in road_network.get_neighbors(curr_city):
            # calculate temp g(n)
            temp = g_n[curr_city] + distance
            # updat the values
            if neighbor not in g_n or temp < g_n[neighbor]:
                originating_city[neighbor] = curr_city
                g_n[neighbor] = temp
                heapq.heappush(priorityQ, (temp, neighbor))

    return []

# print Final path
def reconstruct_path(originating_city, curr_city):
    final_path = [curr_city]
    while curr_city in originating_city:
        curr_city = originating_city[curr_city]
        final_path.append(curr_city)
    final_path.reverse()
    return final_path
