# ToxicSense

A tool to visualize toxicity in social media.

There are two parts:
1. Web application
    Live: https://www.toxicsense.com
    Code: CODE/ToxicSense
2. Chrome extension
    Live: https://chrome.google.com/webstore/detail/toxicsense/nfcggdampbbiejnnnfflnpppknbdhlla
    Code: CODE/ToxicSense-extensions

### Document Overview
In this document, we give instructions on how to run the web application locally, as well as train, build, and make sample predictions with our machine learning toxic comment classifier.

# Section 1: The Web Application


## Quick Start

$ cd CODE/ToxicSense
$ mkvirtualenv --python=`which python3` toxicsense-venv-1
$ pip install -r requirements.txt
$ python manage.py runserver localhost:8000

Visit http://localhost:8000/

Quick start does not include background processing.
To set it up, follow the detailed installation instructions below.

## Full Installation

1. $ cd CODE/ToxicSense
2. Create a python3 virtual environment and activate it. Follow instructions here https://docs.python.org/3/library/venv.html.
    - Or if you have virtualenvwrapper,
    $ mkvirtualenv --python=`which python3` toxicsense-venv-1
3. Install the requirements by running 
    $ pip install -r requirements.txt
4. Run the migrations
    $ python manage.py migrate
5. Install rabbitmq: Follow instructions here https://www.rabbitmq.com/download.html.
    If you are on mac,
    $ brew install rabbitmq
6. Start the rabbitmq server in a separate terminal using 
    $ rabbitmq-server
7. Go to ToxicSense folder in a separate tab/terminal(follow step 1) and start the celery worker and beat
    $ celery -A ToxicSense worker -l info -B
8. Go to ToxicSense folder and start the server. Ignore the warnings about migrations.
    $ python manage.py runserver localhost:8000
9. Visit http://localhost:8000/

Note: If you are on a Mac and you see some weird errors about Objective C, you may need to run `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` from your terminal. It has something to do with the twitter scraper not playing well with python3 on MacOS.

# Section 2: Machine Learning

### Toxicity Prediction
We include instruction for two tasks related to predicting toxicity in tweets, the first, is training the machine learning classifier we use in production and exporting it. The second, is using those saved files to run toxicity prediction from the command line. We've included a saved version of model in case you don't have the time to train the model yourself!

#### Train our Char-CNN Deep Learning Model
1. If haven't already run:
    $ cd CODE/ToxicSense
    $ mkvirtualenv --python=`which python3` toxicsense-venv-1
    $ pip install -r requirements.txt
    do that now...
2. Go to https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data and download train.csv into a directory called "kaggle"
    The file may be zipped, so make sure to use 'unzip' to decompress it.
3. Run all the cells in the build-and-export.ipynb notebook.
    You may need to install Jupyter notebooks: http://jupyter.org/install 
    $ jupyter notebook
4. train-and-export.ipynb will export our model into the directory, "ascii-3-model/"


#### Make Predictions Locally via Command Line
1. Have the project dependencies installed (step one, previous section)
2. Run the following command in bash
    $ python make_prediction.py <tweet>
    for instance you could run,
    $ python make_prediction "Thats one small step for a man, one giant leap for mankind"
The toxicity, along with whether the tweet is obsene, a threat, an insult, or identity hate  will be printed. 
For each category, the prediction is a number between 0 and 1. Where 0 is not a member of the cateogry, and 1 is likely to be a member of the category
