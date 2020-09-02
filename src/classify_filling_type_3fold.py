#!/usr/bin/python3
import pyAudioAnalysis
from pyAudioAnalysis import audioTrainTest as aT
import plotly.subplots
import os, argparse, sys

def train_fold(fold_no):

    data_folders = [dataset_path+"/train"+str(fold_no)+"/fi"+str(i) for i in range(4)]

    aT.extract_features_and_train(data_folders, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "svm", model_name, False)

def test_fold(fold_no):

    test_folders = [dataset_path+"/test"+str(fold_no)+"/fi"+str(i) for i in range(4)]

    cm, thr_prre, pre, rec, thr_roc, fpr, tpr = aT.evaluate_model_for_folders(test_folders, model_name, "svm", "fi1")


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    # required
    parser.add_argument('-d', '--datapath', help='Path of the dataset wrt current working directory.', required=True)
    parser.add_argument('-m', '--modelname', help='Name of the model, used for output names.', required=True)
    # optional
    # TODO: implement quiet option
    parser.add_argument('-q', '--quiet', help='Print nothing but the result.', action='store_true')

    args = parser.parse_args()

    dataset_path = args.datapath

    # TODO: reduce repetitions, reuse features?
    for i in range(3):
        model_name = args.modelname+str(i)
        train_fold(i)
        test_fold(i)

    print("il finito")
