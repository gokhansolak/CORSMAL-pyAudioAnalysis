#!/usr/bin/python3
import pyAudioAnalysis
from pyAudioAnalysis import audioTrainTest as aT
import plotly.subplots
import os, argparse, sys
import pandas as pd

class_code_dict = {'fi':{'name':'Filling type', 'count':4}, 'fu': {'name':'Filling level [%]', 'count':3}}

def train():

    data_folders = [dataset_path+"/train/"+args.classcode+str(i) for i in range(class_count)]

    aT.extract_features_and_train(data_folders, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, args.algorithm, model_name, False)

def predict(object_no):
    # create empty array (column) for each name
    results_dict = {name:[] for name in columns_names}

    i=0
    while(i<200):
        seq_no = str(i).zfill(4)
        fname=dataset_path+"/test/o"+str(object_no)+"_"+seq_no+"_audio.wav"

        # file count may vary, be safe
        if not os.path.exists(fname):
            break;

        c, p, probs_names = aT.file_classification(fname, model_name, args.algorithm)

        results_dict['Object'].append(object_no)
        results_dict['Sequence'].append(seq_no)
        results_dict[class_name].append(c)
        # class probabilities
        for k in range(class_count):
            results_dict[class_name+' prob'+str(k)].append(p[k])

        print("classified obj"+str(object_no)+" "+seq_no+" : "+str(c))
        i+=1

    return pd.DataFrame(results_dict)

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    # required
    parser.add_argument('-d', '--datapath', help='Path of the dataset wrt current working directory.', required=True)
    parser.add_argument('-m', '--modelname', help='Name of the model, used for output names.', required=True)
    parser.add_argument('-c', '--classcode', help='Code of the class identifier (fi, fu). Default: fi.', default='fi')
    parser.add_argument('-a', '--algorithm', help='Classifier: svm, svm_rbf, randomforest... Default: svm.', default='svm')

    # optional
    # TODO: implement quiet option
    parser.add_argument('-q', '--quiet', help='Print nothing but the result.', action='store_true')

    args = parser.parse_args()

    dataset_path = args.datapath

    model_name = args.modelname
    class_name = class_code_dict[args.classcode]['name']
    class_count = class_code_dict[args.classcode]['count']

    train()
    columns_names=["Object", "Sequence", class_name] + [class_name+" prob"+str(i) for i in range(class_count)]
    df = pd.DataFrame(columns=columns_names)

    for obj in [10,11,12]:
        df_obj = predict(obj)
        df = pd.concat([df, df_obj])

    df.to_csv(model_name+'_result.csv', index=False)

    print("il finito")
