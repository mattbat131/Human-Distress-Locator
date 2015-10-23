import arff
import codecs
import new_knn
from math import ceil
from random import shuffle
from itertools import zip_longest


def load_and_shuffle():
    file = codecs.open("HumanDistress_Normalize.arff", 'rb', 'utf-8')
    arff_everything = arff.load(file)
    data_set = arff_everything['data']
    return shuffle(data_set)


def create_k_folds(data, k_folds):
    items_per_fold = ceil(len(data) / k_folds)
    return zip_longest(data, items_per_fold)


def main():
    data = load_and_shuffle()
    k_folds = 10
    folds = create_k_folds(data, k_folds)
    for i in range(len(folds)):
        fold_under_test = folds[i]
        folds_in_database = folds[:i] + folds[i+1:]
    # you figure out the rest, i'm going to bed
