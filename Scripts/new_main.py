import arff
import codecs
import new_knn
from math import ceil
import random
from itertools import zip_longest


def load_and_shuffle():
    file = codecs.open("HumanDistress_Normalize_cleaned.arff", 'rb', 'utf-8')
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


def main():
    data = load_and_shuffle()
    k_folds = 10
    folds = create_k_folds(data, k_folds)
    all_results = dict()
    all_results['true_pos'] = 0
    all_results['false_pos'] = 0
    all_results['true_neg'] = 0
    all_results['false_neg'] = 0
    for i in range(len(folds)):
        fold_under_test = folds[i]
        folds_in_database = folds[:i] + folds[i+1:]
        for point in fold_under_test:
            result = new_knn.k_nearest_neighbor(point, folds_in_database, 9)
            print(result, point[-1])
            if is_positive_class(result):
                if is_positive_class(point[-1]):
                    all_results['true_pos'] += 1
                    print('true_pos')
                else:
                    all_results['false_pos'] += 1
                    print('false_pos')
            else:
                if is_positive_class(point[-1]):
                    all_results['false_neg'] += 1
                    print('false_neg')
                else:
                    all_results['true_neg'] += 1
                    print('true_neg')
            # all_results["result"].append(result)
            # all_results["actual"].append(point[-1])
    report_accuracy(all_results)



if __name__ == "__main__":
    main()
