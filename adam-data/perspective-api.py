#!/bin/python

import os
import csv
import json
from googleapiclient import discovery




def get_tweet_toxicity(tweet, service):
    analyze_request = {
          'comment': { 'text': tweet },
          'requestedAttributes': {'TOXICITY': {}}
    }
    response = service.comments().analyze(body=analyze_request).execute()
    return list(response.get('attributeScores').get('TOXICITY').get('summaryScore').values())

def read_in_file(ffile):
    rows = []
    with open(ffile, 'r') as f:
        csv_file = csv.reader(f)
        next(csv_file)
        for row in csv_file:
            rows = rows + [row]
    return rows

def grab_all_tweets(ffiles):
    res = []
    for ff in ffiles:
        print(ff)
        res = res + read_in_file(ff)
        print(len(res))
    return res




def run_perspective_api(file_out,
                        service,
                        n_out):
    files = [f'user-tweets/{x}' for x in os.listdir("user-tweets") if x.endswith('.csv')]

    all_tweets = grab_all_tweets(files)
    if n_out is None:
        n_out = len(all_tweets)

    output = []

    for i,recs in enumerate(all_tweets[:n_out]):
        user, timestamp, tweet  = recs[0], recs[1], recs[2]
        print(i)
        try:
            tox, tox_label = get_tweet_toxicity(tweet, service)
        except:
            print(f'missing label for {i}') 
            tox, tox_label = 'NA', 'NA'

        output = output + [[user,timestamp, tweet, tox, tox_label]]

    with open(file_out, 'w') as f:
        csv_file = csv.writer(f)
        csv_file.writerow(['username',
                           'timestamp',
                           'tweet',
                           'tox',
                           'toxlabel'])

        for row in output:
            csv_file.writerow(row)

if __name__ == '__main__':
    file_out='toxic-labelled.csv'
    API_KEY=open('papi_key').read()
    service = discovery.build('commentanalyzer',
                              'v1alpha1',
                              developerKey=API_KEY)
    run_perspective_api(file_out,
                        service,
                        None)





