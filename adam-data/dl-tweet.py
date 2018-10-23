import argparse
import csv
import re
from unidecode import unidecode
from twitterscraper import query_tweets

def clean_tweet(tweet):
    tweet_ascii = unidecode(tweet)
    clean_text = re.sub(',','',tweet_ascii)
    return re.sub('\n','', clean_text)

def get_user_tweets(user,limit=2000):
    search_term = '@' + user
    for tweet in query_tweets(search_term, limit):
        if user == tweet.user:
            yield [tweet.user,tweet.timestamp, clean_tweet(tweet.text)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("user", help="download this users tweets")
    parser.add_argument("file", help="dump the contents into this file")
    args = parser.parse_args()

    output_file = args.file
    username = args.user
    with open(output_file, "w", newline = '') as f:
        csv_out = csv.writer(f)
        csv_out.writerow(("username","time","tweet"))
        for row in get_user_tweets(username):
            csv_out.writerow(row)
