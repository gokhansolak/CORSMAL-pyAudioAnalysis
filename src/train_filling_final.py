#!/usr/bin/python3
import sys
sys.path.insert(0, './pyAudioAnalysis')  # nopep8
import random
import numpy as np
import pyAudioAnalysis
from pyAudioAnalysis import audioTrainTest as aT
import plotly.subplots
import os, argparse, sys
import pandas as pd
import filling_analysis_common as filling


def train(train_path):
    data_folders = [os.path.join(train_path,args.classcode+str(i)) for i in range(class_count)]
    aT.extract_features_and_train(
        data_folders, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, args.algorithm, model_name, False
    )

def set_seed(seed=1337):
    random.seed(seed)
    np.random.seed(seed)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # required
    parser.add_argument('-d', '--datapath', help='Path of the dataset w.r.t. current working directory.', required=True)
    parser.add_argument('-m', '--modelname', help='Name of the model, used for output names.', required=True)
    parser.add_argument('-c', '--classcode', help='Code of the class identifier (fi, fu).', required=True)
    parser.add_argument('-a', '--algorithm', help='Classifier: svm, svm_rbf, randomforest...', default='randomforest')

    args = parser.parse_args()

    dataset_path = args.datapath

    model_name = args.modelname
    if args.classcode == 'fi':
        class_name = 'Filling type'
        class_count = 4
    elif args.classcode == 'fu':
        class_name = 'Filling level [%]'
        class_count = 3
    else:
        raise NotImplementedError

    #train
    set_seed()
    train_path = os.path.join(dataset_path, "train")
    train(train_path)

    # create table for results
    column_names=["Object", "Sequence", class_name] + [class_name+" prob"+str(i) for i in range(class_count)]
    df = pd.DataFrame(columns=column_names)

    # test path is more specific
    test_path = os.path.join(dataset_path, "test")

    for obj in [10,11,12]:
        df_obj = filling.predict_object(obj, model_name, args.algorithm, test_path, column_names)
        df = pd.concat([df, df_obj])

    df.to_csv(model_name+'.csv', index=False)

    print("il finito")
