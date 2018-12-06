# ToxicSense

A tool to visualize toxicity in social media.

There are two parts:
1. Web application + Chrome Extension
    1a: Web application
        Live: https://www.toxicsense.com
        Code: ToxicSense
    1b. Chrome extension
        Live: https://chrome.google.com/webstore/detail/toxicsense/nfcggdampbbiejnnnfflnpppknbdhlla
        Code: ToxicSense-extensions

2. Machine Learning Model for toxicity classification


# Document Overview
In this document, we give instructions on how to run the web application locally, as well as train, build, and make sample predictions with our machine learning toxic comment classifier.

# Section 1: The Web Application

## Quick Start

https://developer.twitter.com/content/developer-twitter/en.html
Create a dev account and get required API Keys and fill them in ToxicSense/data_fetch_helpers/creds.py

$ cd ToxicSense
Create a python3 virtual environment and activate it. Follow instructions here https://docs.python.org/3/library/venv.html.
Or if you have virtualenvwrapper,
$ mkvirtualenv --python=`which python3` toxicsense-venv
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver localhost:8000

Visit http://localhost:8000/

Quick start does not include background processing which stores the retrieved tweets in database for future use.
To set it up, follow the detailed installation instructions below.

## Full Installation

1. $ cd ToxicSense
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
    $ python manage.py runserver localhost:8000 --settings=ToxicSense.local_celery_settings
9. Visit http://localhost:8000/

Note: If you are on a Mac and you see some weird errors about Objective C, you may need to run `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` from your terminal. It has something to do with the twitter scraper not playing well with python3 on MacOS.

# Section 2: Machine Learning

## Toxicity Prediction
We include instruction for two tasks related to predicting toxicity in tweets, the first, is training the machine learning classifier we use in production and exporting it.
The second, is using those saved files to run toxicity prediction from the command line.

## Quick Start

We have a trained model saved to immediately test the toxic classifier. 
To run prediction against a tweet,

$ cd create-model
$ mkvirtualenv --python=`which python3` toxicsense-test-model
$ pip install -r test-requirements.txt
$ python make_prediction.py <tweet>
for instance you could run,
$ python make_prediction.py "Thats one small step for a man, one giant leap for mankind"

The toxicity, along with whether the tweet is obsene, a threat, an insult, or identity hate  will be printed. 
For each category, the prediction is a number between 0 and 1. Where 0 is not a member of the category, and 1 is likely to be a member of the category


## Train our Char-NN Deep Learning Model

1. Install virtualenv and install necessary libraries.
    $ cd create-model
    $ mkvirtualenv --python=`which python3` toxicsense-train-model
    $ pip install -r train-requirements.txt
2. We took the data from https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data
    But for quick download, we have uploaded the train file in https://s3.amazonaws.com/toxicsense-submission/train.csv
    Download the file and keep in home folder.
3. Run jupyter notebook.
    $ jupyter notebook
4. Run all the cells in the build-and-export.ipynb notebook.
5. build-and-export.ipynb will export our model into the directory, "ascii-3-model/"

Follow Quick Start to run the model.


## Deployment

We currently use AWS ElasticBeanstalk for deployment.
Below is the link to the tutorial that was followed to make the deployment..
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html


First time:
$ eb init -p python-3.6 toxic-sense
$ eb create env

For successive deployments, 
$ eb deploy

#### SSH into machine

$ eb ssh 

To get into the folder:
From https://stackoverflow.com/a/20070161:

SSH login to Linux
(optional may need to run sudo su - to have proper permissions)
Run `source /opt/python/run/venv/bin/activate`
Run `source /opt/python/current/env`
Run `cd /opt/python/current/app`
Run `python manage.py <commands>`
Or, you can run command as like the below:

Run `cd /opt/python/current/app`
Run `/opt/python/run/venv/bin/python manage.py <command>`
