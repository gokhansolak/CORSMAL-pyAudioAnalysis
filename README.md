# CORSMAL Challenge Audio-only Analysis

Analyzing filling type & level task of the [CORSMAL challenge](http://corsmal.eecs.qmul.ac.uk/containers_manip.html) with only the audio modality using [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis) library.
I wrote this code as a part of the team "Because It's Tactile".
The rest of our team's code resides in [v-iashin/CORSMAL](https://github.com/v-iashin/CORSMAL) repository, please check it. Our team won the CORSMAL challenge in [2020 Intelligent Sensing Summer School](http://cis.eecs.qmul.ac.uk/school2020.html)!


### Validation set analysis

`gather_validation_dataset.sh` puts the _wav_ files into a structured folder, separating classes, as expected by [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis) library:

```
chmod +x gather_validation_dataset.sh
gather_validation_dataset.sh <source data path> <target data path> <class code>
```

_Data paths_ should be specified w.r.t. the current working directory of the terminal. You can call it from another folder.
The expected folder structures are shown at the end of this file.
Killing the script in the middle may change the current directory.

Then, the training and 3-fold validation sequence can be run using `train_filling_validation.py`:
```
python3 src/train_filling_validation.py -d <target data path> -m model_name -c <class code> -a <algorithm>
```
Usage (fi: filling type, fu: filling level):
```
train_filling_validation.py [-h] -d DATAPATH -m MODELNAME
                                   [-c CLASSCODE] [-a ALGORITHM]

optional arguments:
  -h, --help            show this help message and exit
  -d DATAPATH, --datapath DATAPATH
                        Path of the dataset wrt current working directory.
  -m MODELNAME, --modelname MODELNAME
                        Name of the model, used for output names.
  -c CLASSCODE, --classcode CLASSCODE
                        Code of the class identifier (fi, fu). Default: fi.
  -a ALGORITHM, --algorithm ALGORITHM
                        Classifier: svm, svm_rbf, randomforest... Default:
                        svm.
```

When run, it will extract audio features, tune model parameters automatically and finally output some useful statistics about the model performance.
It is happening with minimal code, thanks to pyAudioAnalysis library!

My results on the CORSMAL challenge data can be found in the _results/validation_ folder.
Randomforest classifier gets ~94% on the filling type, ~70% accuracy on the filling level task.

### Final analysis

For final analysis on the test set, we use `gather_final_dataset.sh` instead of `gather_validation_dataset`, because the target folder structure changes:

```
chmod +x gather_dataset.sh
gather_dataset.sh <source data path> <target data path> <class code>
```
The usage is the same as in validation.

Then, the training and prediction sequence can be run using `train_filling_final.py`:
```
python3 src/train_filling_final.py -d <target data path> -m model_name -c <class code> -a <algorithm>
```

Again, the usage is the same as above. It will save a _csv_ file named as "model_name.csv" that contains the case ids and predicted labels and the confidence probabilities.
We output the probabilities, so that we can ensemble the results with another model later.
Our final CORSMAL predictions are compiled using the `main.py` file in [v-iashin/CORSMAL](https://github.com/v-iashin/CORSMAL) repository.

### Ensemble methods

We ensemble the outputs of multiple models developed by our team. The other models are [here](https://github.com/v-iashin/CORSMAL).
We tried multiple combinations with different strategies (see *src/combine_filling_results.py* file).
The *averaging* strategy improved both *filling type* and *filling level* task performances.

In validation set, for *filling level*, *vggish* model achieves a 75.5% accuracy, when ensemble with *pyAudioAnalysis/randomforest* and *r(2+1)d* models, it increases to 78.4%. You can find the outputs of these models in the _results/validation_ folder.


### Folder structures

The source data path should have the audio data from the [challenge](http://corsmal.eecs.qmul.ac.uk/containers_manip.html):
```
├── 1
│   └── audio
├── 2
│   └── audio
├── 3
│   └── audio
├── 4
│   └── audio
├── 5
│   └── audio
├── 6
│   └── audio
├── 7
│   └── audio
├── 8
│   └── audio
├── 9
│   ├── audio

```

The training folder created by `gather_validation_dataset` will look like this (`fi*` are the classes):
```
├── test0
│   ├── fi0
│   ├── fi1
│   ├── fi2
│   └── fi3
├── test1
│   ├── fi0
│   ├── fi1
│   ├── fi2
│   └── fi3
├── test2
│   ├── fi0
│   ├── fi1
│   ├── fi2
│   └── fi3
├── train0
│   ├── fi0
│   ├── fi1
│   ├── fi2
│   └── fi3
├── train1
│   ├── fi0
│   ├── fi1
│   ├── fi2
│   └── fi3
└── train2
    ├── fi0
    ├── fi1
    ├── fi2
    └── fi3
```
