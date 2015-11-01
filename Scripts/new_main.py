import arff
import codecs
import new_knn
from math import ceil
import random
from itertools import zip_longest


def load_and_shuffle():
    file = codecs.open("HumanDistress_Normalize_clean3_featureSelected.arff", 'rb', 'utf-8')
    arff_everything = arff.load(file)
    data_set = arff_everything['data']
    random.shuffle(data_set)
    return data_set

def create_k_folds(data, k_folds):
    items_per_fold = ceil(len(data) / k_folds)
    data_fold = []
    last = 0.0

    while last < len(data):
        data_fold.append(data[int(last):int(last+items_per_fold)])
        last += items_per_fold

    return data_fold


def is_positive_class(class_result):
    return 'Human' in class_result


def report_accuracy(all_results):
    print(all_results)


def frange(x, y, jump):
  while x < y:
    yield x
    x += jump


def main():
    data = load_and_shuffle()
    k_folds = 10
    classes = ('Human', 'Other')
    folds = create_k_folds(data, k_folds)
    all_results = dict()
    all_results['true_pos'] = 0
    all_results['false_pos'] = 0
    all_results['true_neg'] = 0
    all_results['false_neg'] = 0

    for train_or_test in range(2):
        if train_or_test == 0:
            t_folds = folds[:-1]
            print("Training")
        else:
            t_folds = [folds[-1]]
            print("Testing")
        for positive_class_threshold in frange(0.1, 0.451, 0.05):
            k = 5

            for i in range(len(t_folds)):
                #print(i)
                if train_or_test == 0:
                    fold_under_test = t_folds[i]
                    folds_in_database = t_folds[:i] + t_folds[i+1:]
                else:
                    fold_under_test = t_folds[i]
                    folds_in_database = folds[:-1]
                for point in fold_under_test:
                    result = new_knn.k_nearest_neighbor(point, folds_in_database, k, classes, positive_class_threshold)
                    if is_positive_class(result):
                        if is_positive_class(point[-1]):
                            all_results['true_pos'] += 1
                        else:
                            all_results['false_pos'] += 1
                    else:
                        if is_positive_class(point[-1]):
                            all_results['false_neg'] += 1
                        else:
                            all_results['true_neg'] += 1
            print("k = ", k)
            print("positive class threshold =", positive_class_threshold)
            report_accuracy(all_results)
            all_results['true_pos'] = 0
            all_results['false_pos'] = 0
            all_results['true_neg'] = 0
            all_results['false_neg'] = 0



if __name__ == "__main__":
    main()
