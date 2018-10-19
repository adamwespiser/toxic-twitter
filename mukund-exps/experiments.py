import twitter

import creds


CONSUMER_KEY = creds.CONSUMER_KEY
CONSUMER_SECRET = creds.CONSUMER_SECRET

ACCESS_TOKEN = creds.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = creds.ACCESS_TOKEN_SECRET


api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)


def verify_creds():
    print(api.VerifyCredentials())


def print_user_tweets(user):
    results = api.GetUserTimeline(screen_name=user)
    for i, result in enumerate(results):
        print(i)
        print(result.created_at)
        print(result.text)
        print(result.hashtags)
        print(result)
        print('--')


print_user_tweets("realDonaldTrump")

def print_replies(since_id):
    resp = api.GetReplies(since_id=since_id)
    print(resp)
    for r in resp:
        print('--')
        print(type(r))
        print(r)


print_replies("1049292375330361345")
