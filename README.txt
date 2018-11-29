### ToxicSense

A tool to visualize toxicity in social media.

There are two parts:
1. Web application
    Live: https://www.toxicsense.com
    Code: CODE/ToxicSense
2. Chrome extension
    Live: https://chrome.google.com/webstore/detail/toxicsense/nfcggdampbbiejnnnfflnpppknbdhlla
    Code: CODE/ToxicSense-extensions


### Installation

## Quick Start

$ cd CODE/ToxicSense
$ mkvirtualenv --python=`which python3` toxicsense-venv-1
$ pip install -r requirements.txt
$ python manage.py runserver localhost:8000

Visit http://localhost:8000/

Quick start does not include background processing.
To set it up, follow the detailed installation instructions below.

### Installation

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
