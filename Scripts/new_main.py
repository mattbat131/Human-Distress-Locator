import arff
import codecs
import new_knn
from math import ceil
import random
from itertools import zip_longest


def load_and_shuffle():
    file = codecs.open("HumanDistress_Normalize.arff", 'rb', 'utf-8')
    arff_everything = arff.load(file)
    data_set = arff_everything['data']
    return sorted(data_set, key=lambda k: random.random())

def create_k_folds(data, k_folds):
    items_per_fold = ceil(len(data) / k_folds)
    data_fold = []
    last = 0.0

    while last < len(data):
        data_fold.append(data[int(last):int(last+items_per_fold)])
        last += items_per_fold

    return data_fold

def main():
    data = load_and_shuffle()
    k_folds = 10
    folds = create_k_folds(data, k_folds)
    for i in range(len(folds)):
        fold_under_test = folds[i]
        folds_in_database = folds[:i] + folds[i+1:]
        result = list()
        for point in folds[i]:
            result.append(new_knn.k_nearest_neighbor(folds_in_database, folds[i], 10))
        print(result)
    # you figure out the rest, i'm going to bed

if __name__ == "__main__":
    main()
