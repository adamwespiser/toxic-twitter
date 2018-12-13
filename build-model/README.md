## Section 2: Machine Learning

### Toxicity Prediction
We include instruction for two tasks related to predicting toxicity in tweets. The first, is training the machine learning classifier we use in production and exporting it.
The second, is using those saved files to run toxicity prediction from the command line.

### Quick Start

We have a trained model saved to immediately test the toxic classifier. 
To run prediction against a tweet,

$ cd build-model\
$ mkvirtualenv --python=`` `which python3` `` toxicsense-test-model\
$ pip install -r test-requirements.txt\
$ python make_prediction.py <tweet>\
for instance you could run,\
$ python make_prediction.py "Thats one small step for a man, one giant leap for mankind"

The toxicity, along with whether the tweet is obsene, a threat, an insult, or identity hate  will be printed. 
For each category, the prediction is a number between 0 and 1. Where 0 is not a member of the category, and 1 is likely to be a member of the category


### Train our Char-NN Deep Learning Model

1. Install virtualenv and install necessary libraries.\
    $ cd build-model\
    $ mkvirtualenv --python=`` `which python3` `` toxicsense-train-model\
    $ pip install -r train-requirements.txt
2. We took the data from https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data\
    Download the file `train.csv` and keep in home folder.
3. Run jupyter notebook.\
    $ jupyter notebook
4. Run all the cells in the build-and-export.ipynb notebook.
5. build-and-export.ipynb will export our model into the directory, "ascii-3-model/"

Note: This step will take you 3-4 hours, depending on your computer, and the notebook was run on a computer with a discrete GPU.

Follow Quick Start to run the model.
