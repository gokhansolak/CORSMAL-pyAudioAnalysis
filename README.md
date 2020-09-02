# CORSMAL Challenge Audio-only Analysis

Analyzing different tasks of the [CORSMAL challenge](http://corsmal.eecs.qmul.ac.uk/containers_manip.html) using only the audio modality.

`gather_dataset.sh` puts the _wav_ files into a structured folder, as expected by [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis) library:

```
gather_dataset <source data path> <target data path>
```

_Data paths_ should be specified w.r.t. the current working directory of the terminal. You can call it from another folder. Killing the script in the middle may change the current directory.

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
