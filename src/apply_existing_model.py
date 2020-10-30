#!/usr/bin/python3
import sys
sys.path.insert(0, './pyAudioAnalysis')  # nopep8
# takes an already trained pyAudioAnalysis model and predicts the
# audio file classes in the given folder
import pyAudioAnalysis
from pyAudioAnalysis import audioTrainTest as aT
import plotly.subplots
import os, argparse, sys
import pandas as pd
import filling_analysis_common as filling


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    # required
    parser.add_argument('-d', '--datapath', help='Path of the test set wrt current working directory.', required=True)
    parser.add_argument('-m', '--modelname', help='Name of the model, used for output names.', required=True)
    parser.add_argument('-c', '--classcode', help='Code of the class identifier (fi, fu)', required=True)
    parser.add_argument('-a', '--algorithm', help='Classifier: svm, svm_rbf, randomforest...', default='randomforest')
    parser.add_argument('-s', '--predict_on_private', help='If True also makes preds for private subset',
                        action='store_true', default=False)

    # optional
    parser.add_argument('-v', '--validation', help='3-fold validation.', action='store_true')

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

    column_names=["Object", "Sequence", class_name] + [class_name+" prob"+str(i) for i in range(class_count)]
    df = pd.DataFrame(columns=column_names)

    if args.validation:
        test_objects = [[3,6,9],[1,4,7],[2,5,8]]

        for fold_no in [0,1,2]:
            print("fold "+str(fold_no))

            for obj in test_objects[fold_no]:
                df_obj = filling.predict_object(obj, model_name+str(fold_no), args.algorithm, dataset_path+str(fold_no), column_names)
                df = pd.concat([df, df_obj])
        df.to_csv(model_name+'_result.csv', index=False)
    else:
        for obj in [10,11,12]:
            df_obj = filling.predict_object(obj, model_name, args.algorithm, dataset_path, column_names)
            df = pd.concat([df, df_obj])
        df.to_csv(model_name+'_result_public_test.csv', index=False)

        if args.predict_on_private:
            # init the dataset again
            df = pd.DataFrame(columns=column_names)
            for obj in [13,14,15]:
                df_obj = filling.predict_object(obj, model_name, args.algorithm, dataset_path, column_names)
                df = pd.concat([df, df_obj])
            df.to_csv(model_name+'_result_private_test.csv', index=False)

    print("il finito")
