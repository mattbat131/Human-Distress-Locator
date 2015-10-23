import heapq
from math import sqrt
from statistics import mode

class neighbor_item:
    def __init__(self, data, distance):
        self.data = data
        self.distance = distance

    def __lt__(self, other):
        return self.distance < other.distance


def default_get_class_function(neighbor):
    return neighbor.data[-1]


def euclidean_distance_function(one, two):
    all_dimensions = zip(one, two)
    squared_distance = 0
    for dimension in all_dimensions:
        if isinstance(dimension[0], float) and isinstance(dimension[1], float):
            squared_distance += (dimension[0] - dimension[1]) ** 2
    return sqrt(squared_distance)


def k_nearest_neighbor(query, data_set, k,
                       distance_function=euclidean_distance_function,
                       get_class_function=default_get_class_function,
                       compute_winning_class_function=mode):
    all_neighbors_heap = []
    for point in data_set:
        distance = distance_function(query, point)
        new_neighbor = neighbor_item(point, distance)
        heapq.heappush(all_neighbors_heap, new_neighbor)
    top_neighbors = [heapq.heappop(all_neighbors_heap) for i in range(k)]
    classes = [get_class_function(neighbor) for neighbor in top_neighbors]
    return compute_winning_class_function(classes)