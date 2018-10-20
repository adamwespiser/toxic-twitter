#!/bin/bash
# code is modified from the following repo
#git clone git@github.com:kennethreitz/twitter-scraper.git
#

# to run a new example, you need to figure out how many pages
# (second arg) are needed,
# if you specify too many, there will be an error (need to fix this)

python twitter-scraper/download-user-tweets.py CrownUncrowned 8
python twitter-scraper/download-user-tweets.py realDonaldTrump 35
python twitter-scraper/download-user-tweets.py ItsLilbaby_1 10
python twitter-scraper/download-user-tweets.py Anthony862 39
python twitter-scraper/download-user-tweets.py dseddon91 35
python twitter-scraper/download-user-tweets.py DerryIrvine 35
python twitter-scraper/download-user-tweets.py _Whtsrfce 32
