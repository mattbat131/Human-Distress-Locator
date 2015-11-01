import heapq
from math import sqrt
from statistics import mode, mean, StatisticsError

class neighbor_item:
    def __init__(self, data, distance):
        self.data = data
        self.distance = distance

    def __lt__(self, other):
        return self.distance < other.distance


def default_get_class_function(neighbor):
    return neighbor.data[-1]


# def find_two_class_labels(neighbors, get_class_function):
#     a_class = get_class_function(neighbors[0])
#     b_class = a_class
#     for neighbor in neighbors:
#         if get_class_function(neighbor) is not a_class:
#             b_class = get_class_function(neighbor)
#             break
#     return a_class, b_class


def euclidean_distance_function(one, two):
    all_dimensions = zip(one, two)
    squared_distance = 0
    for dimension in all_dimensions:
        if isinstance(dimension[0], float) and isinstance(dimension[1], float):
            squared_distance += (dimension[0] - dimension[1]) ** 2
    return sqrt(squared_distance)


def average_filtered_mode(top_neighbors, get_class_function, classes, positive_class_threshold):
    sum = 0
    for neighbor in top_neighbors:
        sum += neighbor.distance
    avg = sum/len(top_neighbors)

    avg_top_neighbors = [neighbor for neighbor in top_neighbors if neighbor.distance <= avg]

    return mode_based_function(avg_top_neighbors, get_class_function)


# Assumes class labels are binary!!!!!!
def weighted_average_class(top_neighbors, get_class_function, classes, positive_class_threshold):
    weights = [1.0/n.distance for n in top_neighbors if n.distance != 0]
    weight_sum = sum(weights)
    a_class, b_class = classes
    a_class_total = 0
    for i in range(len(top_neighbors)):
        if a_class in get_class_function(top_neighbors[i]):
            a_class_total += weights[i]
    if a_class_total / weight_sum > positive_class_threshold:
        return a_class
    else:
        return b_class


def weighted_euclidian_distance_mean_class(top_neighbors, get_class_function, classes, positive_class_threshold):
    weights = [n.distance**2 for n in top_neighbors]
    weight_sum_sqrt = sqrt(sum(weights))
    a_class, b_class = find_two_class_labels(top_neighbors, get_class_function)
    if a_class is b_class:
        return a_class
    a_class_total = 0
    for i in range(len(top_neighbors)):
        if a_class in get_class_function(top_neighbors[i]):
            a_class_total += weights[i]
    if a_class_total / weight_sum_sqrt > .5:
        return a_class
    else:
        return b_class


def weighted_sqr_mean_class(top_neighbors, get_class_function, classes, positive_class_threshold):
    weights = [sqrt(n.distance) for n in top_neighbors]
    weight_sum = sum(weights)
    a_class, b_class = find_two_class_labels(top_neighbors, get_class_function)
    if a_class is b_class:
        return a_class
    a_class_total = 0
    for i in range(len(top_neighbors)):
        if a_class in get_class_function(top_neighbors[i]):
            a_class_total += weights[i]
    if a_class_total / weight_sum > .5:
        return a_class
    else:
        return b_class


def mode_based_function(top_neighbors, get_class_function,  classes, positive_class_threshold):
    classes = [get_class_function(neighbor) for neighbor in top_neighbors]
    try:
        return mode(classes)
    except StatisticsError:
        return "Human-In-Distress"


# def weighted_avg(top_neighbors, get_class_function=default_get_class_function):
#     for i in len()
#     mean(top_neighbors)

# Classes should be in order of preference (for true positive/false positive weighting)
def k_nearest_neighbor(query, folds, k, classes, positive_class_threshold,
                       distance_function=euclidean_distance_function,
                       get_class_function=default_get_class_function,
                       compute_winning_class_function=weighted_average_class):
    all_neighbors_heap = []
    for fold in folds:
        for point in fold:
            distance = distance_function(query, point)
            new_neighbor = neighbor_item(point, distance)
            heapq.heappush(all_neighbors_heap, new_neighbor)
    top_neighbors = [heapq.heappop(all_neighbors_heap) for i in range(k)]
    return compute_winning_class_function(top_neighbors, get_class_function,
                                          classes, positive_class_threshold)
