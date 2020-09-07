# CORSMAL Challenge pyAudioAnalysis

Analyzing filling type & level task of the [CORSMAL challenge](http://corsmal.eecs.qmul.ac.uk/containers_manip.html) with only the audio modality using [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis) library.
This code is a part of the team "Because It's Tactile".
The rest of our team's code resides in [v-iashin/CORSMAL](https://github.com/v-iashin/CORSMAL) repository, please check it. Our team won the CORSMAL challenge in [2020 Intelligent Sensing Summer School](http://cis.eecs.qmul.ac.uk/school2020.html)!

## Installation

_Tested on Ubuntu 18.04_

1. Clone this repository `git clone --recursive https://github.com/gokhansolak/CORSMAL-pyAudioAnalysis.git` (mind the `--recursive` flag).
2. Follow the [installation guide in pyAudioAnalysis to install dependencies](https://github.com/tyiannak/pyAudioAnalysis#installation). Also make sure `ffmpeg` is installed. Alternatively, you may use `conda` environment (`conda env create -f environment.yml`) which will install a virtual environment with all requirements for `pyAudioAnalysis` and `ffmpeg`.

## Restructure dataset

We provide the scripts for both validation and final set ups. To replicate the results you need just need to run only the lines with `final`. If you would like to experiment with different models you will also need to prepare the folder for validation.

For final analysis on the test set, we use `./gather_final_dataset.sh`. `./gather_final_dataset.sh` puts the _wav_ files into a structured folder, separating classes, as expected by [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis) library.

**Warning:** Dataset paths of different batches (filling type or level, validation or final) must be separate, otherwise the library will confuse the classes. Note that we append `/final/fi` to `<target data path>`

```bash
chmod +x ./gather_final_dataset.sh
# for filling type (fi)
./gather_final_dataset.sh <source data path> <target data path>/final/fi "fi"
# for filling level (fu)
./gather_final_dataset.sh <source data path> <target data path>/final/fu "fu"
# Note that killing the script in the middle may change the current directory.
```

If you would like to experiment with different models, use `./gather_validation_dataset.sh` instead of `./gather_final_dataset.sh`, because the target folder structure changes. Run the following to restructure both validation subsets:
```bash
chmod +x ./gather_validation_dataset.sh
# for filling type (fi)
./gather_validation_dataset.sh <source data path> <target data path>/validation/fi "fi"
# for filling level (fu)
./gather_validation_dataset.sh <source data path> <target data path>/validation/fu "fu"
# Note that killing the script in the middle may change the current directory.
```

The expected source dir structure.
```
<source data path>:
├── [1-9]
│   └── audio
│       └── sSS_fiI_fuU_bB_lL_audio.wav  # SS - subject id, I - fill level, etc
└── [10-12]
    └── audio
        └── XXXX_audio.wav  # OO - object id and XXXX - event id
```

The training folders created by `gather_final/validation_dataset` will look like this (`fi*` or `fu*` are the classes, `train[0-2]` are split ids):
```
<target data path>
├── final
│   ├── fi
│   │   ├── test
│   │   └── train
│   │       └── fi[0-3]
│   └── fu
│       ├── test
│       └── train
│           └── fu[0-2]

and if you extracted validation
<target data path>
└── validation
    ├── fi
    │   ├── test[0-2]
    │   │   └── fi[0-3]
    │   └── train[0-2]
    │       └── fi[0-3]
    └── fu
        ├── test[0-2]
        │   └── fu[0-2]
        └── train[0-2]
            └── fu[0-2]

```

## Make Final Predictions on Test Set

To make the predictions using our pre-trained random forest models, copy the content of `./models` into `./`, and run these lines to apply them to make predictions on objects _10, 11, 12_ (public test set), as follows
```bash
# Run `conda activate pyAudioAnalysis` if you are using conda and replace `python3` with `python`
# for filling level (fu)
python3 ./src/apply_existing_model.py -d <target data path>/final/fu/test -m "flevel-randomforest-final" -c "fu"
# for filling type (fi)
python3 ./src/apply_existing_model.py -d <target data path>/final/fi/test -m "ftype-randomforest-final" -c "fi"
```

It will create `.csv` files in the `./` directory. They should match the ones in `./results`.
We output the probabilities, so that we can ensemble the results with another model later.
Our final CORSMAL predictions are compiled using the `main.py` file in [v-iashin/CORSMAL](https://github.com/v-iashin/CORSMAL) repository.

We blend the outputs of multiple models developed by our team. The other models and the final blending script are in [v-iashin/CORSMAL](https://github.com/v-iashin/CORSMAL).

We tried multiple combinations with different strategies (see *src/combine_filling_results.py* file).
The *averaging* strategy improved both *filling type* and *filling level* task performances.
In validation set, for *filling level*, *vggish* model achieves a 75.5% accuracy, when ensemble with *pyAudioAnalysis/randomforest* and *r(2+1)d* models, it increases to 78.4%. You can find the outputs of these models in the _results/validation_ folder.

## How to Train Another Model

Start by looking for the best hyper-parameters on validation set. The training and 3-fold validation sequence can be run using `./src/train_filling_validation.py`:
```bash
# Run `conda activate pyAudioAnalysis` if you are using conda and replace `python3` with `python`
# for filling type (fi)
python3 ./src/train_filling_validation.py -d <target data path>/validation/fi -m "ftype-my-model" -c "fi"
# for filling level (fu)
python3 ./src/train_filling_validation.py -d <target data path>/validation/fu -m "flevel-my-model" -c "fu"
```
where `<target data path>` is the same path you used to form validation sets. `<model name> (-m)` an arbitrary string which will be appended to results. By default it will train a random forest classifier (run `python3 ./train_filling_validation.py --help` to see more).

When run, it will extract audio features, tune model parameters automatically and finally output some useful statistics about the model performance.
It is happening with minimal code, thanks to pyAudioAnalysis library!

The results on the CORSMAL validation data can be found in the _results/validation/performance_ folder.
Randomforest classifier gets ~94% on the filling type task and ~70% accuracy on the filling level task. Feel free to tune it more.

Then, train your model on the full training dataset (train final) run using `./src/train_filling_final.py`:
```bash
# Run `conda activate pyAudioAnalysis` if you are using conda and replace `python3` with `python`
# for filling type (fi)
python3 ./src/train_filling_final.py -d <target data path>/final/fi -m "ftype-my-model-final" -c "fi"
# for filling level (fu)
python3 ./src/train_filling_final.py -d <target data path>/final/fu -m "flevel-my-model-final" -c "fu"
```
