from twython import Twython
from pymongo import Connection

db = Connection(
    'mongodb://test:test@paulo.mongohq.com:10063/TweetCat').TweetCat


# returns only newly downloaded tweets that fit params, sets them to old
# afterwards
def get_new_tweets(**kwargs):
    download_tweets()
    kwargs.update({'new': True})
    y = []
    for x in db.tweets.find(kwargs):
        x['new'] = False
        db.tweets.save(x)
        y.append(x['text'])
    return y

# returns all tweets that fit params
def get_tweets(**kwargs):
    return [x for x in db.tweets.find(kwargs)]

# returns only the text of all tweets that fit params
def get_tweets_text(**kwargs):
    return [x['text'] for x in db.tweets.find(kwargs)]

# download new tweets from each of the accounts in the databse, setting
# the category
def download_tweets():
    APP_KEY = 'CVP4Tgh3FZahPl6wVSf6NQ'
    APP_SECRET = 'aYbYRnYjbtDzJjTWsqjp10vKbxzSrB46CnuQtwZMI'
    OAUTH_TOKEN = '76013996-9XJdUtMi78dQ3OiFIBuXqziNDVwBK6B1noh4eUu5w'
    OAUTH_TOKEN_SECRET = 'BoihAhEBpydRZJGB5RsUPTPrKTxTzW3Fejr88MFl0'

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    for acc in db.accounts.find():
        i = 1
        total = 0
        # get id of last tweet from that account, to only search for new ones
        lastweet = db.tweets.find(
            {'user': acc['user']}).sort('_id', -1).limit(1)
        lastweet = [x for x in lastweet]
        if len(lastweet) > 0:
            lastweet = lastweet[0]['_id']
        else:
            lastweet = 1
        while True:
            r = twitter.get_user_timeline(
                screen_name=acc['user'], count=200, page=i, since_id=lastweet)
            for x in r:
                db.tweets.save(
                    {'_id': x['id_str'], 'new': True, 'classn': acc['cat'], 'text': x['text'].encode('ascii', 'ignore'), 'user': acc['user']})
            # no more tweets
            if len(r) == 0:
                break
            else:
                i += 1
                total += len(r)

            print 'saved %s tweets from %s' % (total, acc['user'])
        print 'saved all tweets from: %s' % acc['user']


if __name__ == '__main__':

    # para adicionar novas contas rodar: db.accounts.save({'user':NOMEDACONTA,
    # 'cat':NOMEDACATEGORIA})
    download_tweets()
    print "NEW:", len(get_new_tweets()), "TOTAL:", db.tweets.count()
    # 25801
