# ToxicSense

A tool to visualize toxicity in social media.

# Installation

1. Clone this repository.
2. `cd ToxicSense`
3. Create a python3 virtual environment and activate it. Follow instructions here https://docs.python.org/3/library/venv.html.
    - Or if you have virtualenvwrapper, ```mkvirtualenv --python=`which python3` dva-project```
4. Install the requirements by running `pip install -r requirements.txt`
5. Go to ToxicSense folder and start the server with `python manage.py runserver localhost:8000` (Ignore the warnings about migrations)
6. Go to http://localhost:8000/

Note: If you are on a Mac and you see some weird errors about Objective C, you may need to run `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` from your terminal. It has something to do with the twitter scraper not playing well with python3 on MacOS.
