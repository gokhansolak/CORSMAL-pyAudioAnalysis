#!/usr/bin/python3
import sys
sys.path.insert(0, './pyAudioAnalysis')  # nopep8
import random
import numpy as np
import pyAudioAnalysis
from pyAudioAnalysis import audioTrainTest as aT
import plotly.subplots
import os, argparse, sys


def set_seed(seed=1337):
    random.seed(seed)
    np.random.seed(seed)

def train_fold(fold_no):
    data_folders = [dataset_path+"/train"+str(fold_no)+"/"+args.classcode+str(i) for i in range(class_count)]
    aT.extract_features_and_train(
        data_folders, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, args.algorithm, model_name, False
    )

def test_fold(fold_no):
    test_folders = [dataset_path+"/test"+str(fold_no)+"/"+args.classcode+str(i) for i in range(class_count)]
    aT.evaluate_model_for_folders(
        test_folders, model_name, args.algorithm, args.classcode+"1"
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # required
    parser.add_argument('-d', '--datapath', help='Path of the dataset wrt current working directory.', required=True)
    parser.add_argument('-m', '--modelname', help='Name of the model, used for output names.', required=True)
    parser.add_argument('-c', '--classcode', help='Code of the class identifier (fi, fu).', required=True)
    parser.add_argument('-a', '--algorithm', help='Classifier: svm, svm_rbf, randomforest...', default='randomforest')

    args = parser.parse_args()

    dataset_path = args.datapath

    if args.classcode == 'fi':
        class_name = 'Filling type'
        class_count = 4
    elif args.classcode == 'fu':
        class_name = 'Filling level [%]'
        class_count = 3
    else:
        raise NotImplementedError

    set_seed()

    # TODO: reduce repetitions, reuse features?
    for i in range(3):
        model_name = args.modelname+str(i)
        train_fold(i)
        test_fold(i)

    print("il finito")
