#!/usr/bin/python3
import pyAudioAnalysis
from pyAudioAnalysis import audioTrainTest as aT
import os, argparse, sys
import pandas as pd
import re

def predict_object(object_no, model_name, algorithm, dirpath, column_names):
    """Predicts the class for all wav objects in the directory,
        with matching object_no. Uses the trained model with name model_name.

    Args:
        model_name (str): pyAudioAnalysis model name.
        algorithm (str): pyAudioAnalysis algorithm.
        object_no (int): object of the experiment.
        dirpath (str): path of the wav files.
        column_names (list): table column names.

    Returns:
        pd.DataFrame: table of results.

    """
    if not os.path.isdir(dirpath):
        print("Can't find path "+dirpath)

    # create empty array (column) for each name
    results_dict = {name:[] for name in column_names}
    class_name = column_names[2]

    file_pattern="o"+str(object_no)+r"_([\w\d_]+)_audio.wav"

    files = [f for f in os.listdir(dirpath) if re.match(file_pattern, f)]

    print(files)

    for fname in files:
        seq_no = re.match(file_pattern, fname).group(1)

        c, p, probs_names = \
            aT.file_classification(os.path.join(dirpath,fname), model_name, algorithm)

        print(p)

        results_dict['Object'].append(object_no)
        results_dict['Sequence'].append(seq_no)
        results_dict[class_name].append(c)
        # class probabilities
        for k in range(len(p)):
            results_dict[class_name+' prob'+str(k)].append(p[k])

        print("classified obj"+str(object_no)+" "+seq_no+" : "+str(c))

    return pd.DataFrame(results_dict)
