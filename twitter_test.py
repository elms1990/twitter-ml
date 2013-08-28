from twython import Twython
from pymongo import Connection

db = Connection(
    'mongodb://test:test@paulo.mongohq.com:10063/TweetCat').TweetCat


def get_tweets(**kwargs):
    return [x for x in db.tweets.find(kwargs)]


def get_tweets_text(**kwargs):
    return [x['text'] for x in db.tweets.find(kwargs)]


def download_tweets(user, num=20):
    #db.tweets.remove()

    APP_KEY = 'CVP4Tgh3FZahPl6wVSf6NQ'
    APP_SECRET = 'aYbYRnYjbtDzJjTWsqjp10vKbxzSrB46CnuQtwZMI'
    OAUTH_TOKEN = '76013996-9XJdUtMi78dQ3OiFIBuXqziNDVwBK6B1noh4eUu5w'
    OAUTH_TOKEN_SECRET = 'BoihAhEBpydRZJGB5RsUPTPrKTxTzW3Fejr88MFl0'

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    i = 0
    total = 0
    while True:
        r = twitter.get_user_timeline(screen_name=user, count=200, page=i)
        for x in r:
            db.tweets.save(
                {'_id': x['id_str'], 'classn': 'sport', 'text': x['text'].encode('ascii', 'ignore'), 'user': user})
        if len(r) == 0:
            break
        else:
            i += 1
            total += len(r)

        print 'saved %s tweets' % total


if __name__ == '__main__':
    download_tweets('SkySports')
    download_tweets('BBCSport')
    download_tweets('ESPN')

    print len(get_tweets_text())
