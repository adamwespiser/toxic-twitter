### ToxicSense

A tool to visualize toxicity in social media.

### Installation

1. Clone this repository.
2. `cd ToxicSense`
3. Create a python3 virtual environment and activate it. Follow instructions here https://docs.python.org/3/library/venv.html.
    - Or if you have virtualenvwrapper, ```mkvirtualenv --python=`which python3` dva-project```
4. Install the requirements by running `pip install -r requirements.txt`
5. Run the migrations, `python manage.py makemigrations` and then `python manage.py migrate`
6. Install rabbitmq, E.g. `brew install rabbitmq` (Follow instructions here https://www.rabbitmq.com/download.html)
7. Start the rabbitmq server in a separate terminal using `rabbitmq-server`
8. Go to ToxicSense folder in a separate terminal and start the celery worker and beat `celery -A ToxicSense worker -l info -B`
9. Go to ToxicSense folder and start the server with `python manage.py runserver localhost:8000` (Ignore the warnings about migrations)
10. Go to http://localhost:8000/

Note: If you are on a Mac and you see some weird errors about Objective C, you may need to run `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` from your terminal. It has something to do with the twitter scraper not playing well with python3 on MacOS.

### Deployment

We currently use AWS ElasticBeanstalk for deployment.
Below is the link to the tutorial that was followed to make the deployment..
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html


First time:
$ eb init -p python-3.6 toxic-sense-mid --profile=gatech
$ eb create first-env --profile=gatech

For successive deployments, 
$ eb deploy --profile=gatech

## SSH into machine

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
