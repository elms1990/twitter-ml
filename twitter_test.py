from twython import Twython
from pymongo import Connection


def get_tweets(db, **kwargs):
    return [x for x in db.tweets.find(kwargs)]


def download_tweets(db, user, num=20):
    db.tweets.remove()

    APP_KEY = 'CVP4Tgh3FZahPl6wVSf6NQ'
    APP_SECRET = 'aYbYRnYjbtDzJjTWsqjp10vKbxzSrB46CnuQtwZMI'
    OAUTH_TOKEN = '76013996-9XJdUtMi78dQ3OiFIBuXqziNDVwBK6B1noh4eUu5w'
    OAUTH_TOKEN_SECRET = 'BoihAhEBpydRZJGB5RsUPTPrKTxTzW3Fejr88MFl0'

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    r = twitter.get_user_timeline(screen_name=user)

    for x in r:
        db.tweets.save({'_id': x['id_str'], 'classn': user, 'text': x['text']})


if __name__ == '__main__':
	db = Connection(
	    'mongodb://test:test@paulo.mongohq.com:10063/TweetCat').TweetCat
    download_tweets(db, 'ESPN')
    print get_tweets(db, classn='ESPN')
