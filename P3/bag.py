#!usr/bin/python3
"""
This is an implementation of bagging algorithm
Author: Stan Tian, Yimin Chen, Devansh Gupta
"""
import sys
import os
import numpy as np
import mldata
from Bagging_Model import Bagging
from DT_Model import ID3
from LR_Model import LogisticRegression
from NB_Model import NaiveBayes
from evaluation_lib import k_fold_cv

K_FOLD = 5
ID3_Config = [1, False] # depth = 1, not use_gain_ratio = False
NB_Config = [5, 3] # n_bins = 5, m_estimate = 3
LR_Config = [0.01, 100, 0.1] # learning_rate = 0.01, n_iter = 100, lambda=0.1)

def main():
    """
    run the naive bayes network with given command line input
    ----------
    """
    file_path, use_full_sample, learning_algo, n_iter = sys.argv[1:5]
    # parse args
    [use_full_sample, n_iter] = [int(use_full_sample), int(n_iter)]
    examples = get_dataset(file_path)
    param = [parse_learning_algo(learning_algo), n_iter]
    if use_full_sample:
        samples = examples[:, 1:-1]
        targets = examples[:, -1]
        bagg = Bagging(*param)
        bagg.ensemble_fit(samples, targets)
    else:
        avg_vals, std, area_under_roc = k_fold_cv('bag', param, examples, K_FOLD)
        print (("Accuracy: %.3f %.3f " + os.linesep +
                "Precision: %.3f %.3f " + os.linesep +
                "Recall: %.3f %.3f" + os.linesep +
                "Area under ROC: %.3f") % (avg_vals[0], std[0], avg_vals[1], std[1], avg_vals[2], std[2], area_under_roc))

def get_dataset(file_path):
    """
    parse the dataset stored in the input file path
    ----------
    file_path : String
        the path to the dataset
    """
    raw_parsed = mldata.parse_c45(file_path.split(os.sep)[-1], file_path)
    return np.array(raw_parsed, dtype=object)

def parse_learning_algo(lr):
    """
    parses user input and returns corresponding learning algorithm
    ----------
    lr : String
        the learning algo of choice
    """
    models = ['dtree', 'nbayes', 'logreg']
    if lr not in models:
        raise ValueError("Error Code: INPUT ALGORITHM UNAVAILABLE")
    if lr == models[0]:
        return ID3(*ID3_Config)
    elif lr == models[1]:
        return NaiveBayes(*NB_Config)
    elif lr == models[2]:
        return LogisticRegression(*LR_Config)
    else:
        raise Exception("Error Code: UNKNOWN_IO_ERROR")

if __name__ == '__main__':
    main()
