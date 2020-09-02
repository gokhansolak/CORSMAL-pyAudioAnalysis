# CORSMAL Challenge Audio-only Analysis

Analyzing filling type task of the [CORSMAL challenge](http://corsmal.eecs.qmul.ac.uk/containers_manip.html) with only the audio modality using [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis) library.

### 3-fold analysis

`gather_dataset_3fold.sh` puts the _wav_ files into a structured folder, as expected by [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis) library:

```
chmod +x gather_dataset_3fold.sh
gather_dataset_3fold.sh <source data path> <target data path> <class code>
```

_Data paths_ should be specified w.r.t. the current working directory of the terminal. You can call it from another folder. Killing the script in the middle may change the current directory.

Then, the 3-fold classification/test sequence can be run using `classify_filling_type_3fold.py`:
```
python3 src/classify_filling_type_3fold.py -d <target data path> -m model_name -c <class code>
```
Usage (fi: filling type, fu: filling level):
```
classify_filling_type_3fold.py [-h] -d DATAPATH -m MODELNAME -c CLASSCODE [-q]

optional arguments:
  -h, --help            show this help message and exit
  -d DATAPATH, --datapath DATAPATH
                        Path of the dataset wrt current working directory.
  -m MODELNAME, --modelname MODELNAME
                        Name of the model, used for output names.
  -c CLASSCODE, --classcode CLASSCODE
                        Code of the class identifier (fi, fu).
  -q, --quiet           Print nothing but the result.

```

### Final analysis

For final analysis, we use `gather_dataset.sh` instead of `gather_dataset_3fold`:

```
chmod +x gather_dataset.sh
gather_dataset.sh <source data path> <target data path> <class code>
```
The usage is same as in 3-fold.

Then, the classification sequence can be run using `classify_filling_type.py`:
```
python3 src/classify_filling_type.py -d <target data path> -m model_name -c <class code>
```

Again, the usage is the same as the 3-fold above. It will save a _csv_ file named as "model_name_result.csv" that contains the case ids and predicted labels and the confidence probabilities.

### Folder structures

The source data path should have the following, among other things:
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

The resulting dataset folder will look like this (`fi*` are the classes):
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
