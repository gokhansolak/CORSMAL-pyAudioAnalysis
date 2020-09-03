#!/usr/bin/python3
import pyAudioAnalysis
from pyAudioAnalysis import audioTrainTest as aT
import plotly.subplots
import os, argparse, sys
import pandas as pd
import classify_filling_common as filling

class_code_dict = {'fi':{'name':'Filling type', 'count':4}, 'fu': {'name':'Filling level [%]', 'count':3}}

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    # required
    parser.add_argument('-d', '--datapath', help='Path of the dataset wrt current working directory.', required=True)
    parser.add_argument('-m', '--modelname', help='Name of the model, used for output names.', required=True)
    parser.add_argument('-c', '--classcode', help='Code of the class identifier (fi, fu). Default: fi.', default='fi')
    parser.add_argument('-a', '--algorithm', help='Classifier: svm, svm_rbf, randomforest... Default: svm.', default='svm')

    # optional
    # TODO: implement quiet option
    parser.add_argument('-v', '--validation', help='3-fold validation.', action='store_true')

    args = parser.parse_args()

    dataset_path = args.datapath

    model_name = args.modelname
    class_name = class_code_dict[args.classcode]['name']
    class_count = class_code_dict[args.classcode]['count']

    column_names=["Object", "Sequence", class_name] + [class_name+" prob"+str(i) for i in range(class_count)]
    df = pd.DataFrame(columns=column_names)

    if args.validation:
        test_objects = [[3,6,9],[1,4,7],[2,5,8]]

        for fold_no in [0,1,2]:
            print("fold "+str(fold_no))

            for obj in test_objects[fold_no]:
                df_obj = filling.predict_object(obj, model_name+str(fold_no), args.algorithm, dataset_path+str(fold_no), column_names)
                df = pd.concat([df, df_obj])
    else:
        for obj in [10,11,12]:
            df_obj = filling.predict_object(obj, model_name, args.algorithm, dataset_path, column_names)
            df = pd.concat([df, df_obj])

    df.to_csv(model_name+'_result.csv', index=False)

    print("il finito")
