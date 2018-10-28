# OVERVIEW

`toxic-labelled.csv` this contains tweets for select users, along with a toxic score according to perspecitive api.     
`perspective-api.py` is the script used to generate `toxic-labelled.csv`, and it requires `papi_key`, not under git, to contain your peprspective api key. If you don't have one, message me and I will send you the file.     
`user-tweets` is a folder that contains examples of different users I found to have toxic messages.
`run.sh` contains the scripts used to download the tweets it `user-tweets`. There are a couple of different methods/libraries at use.    
`dl-tweet.py` is a script that takes two arguments, the user, and the location to download the tweets.
`twitter-scraper` subdirectory is a a project I tried to download tweets, however, there is an error and it doesn't work every well.
