from twython import Twython
from pymongo import Connection


db = Connection('mongodb://test:test@paulo.mongohq.com:10063/TweetCat').TweetCat

APP_KEY = 'CVP4Tgh3FZahPl6wVSf6NQ'
APP_SECRET = 'aYbYRnYjbtDzJjTWsqjp10vKbxzSrB46CnuQtwZMI'
OAUTH_TOKEN = '76013996-9XJdUtMi78dQ3OiFIBuXqziNDVwBK6B1noh4eUu5w'
OAUTH_TOKEN_SECRET = 'BoihAhEBpydRZJGB5RsUPTPrKTxTzW3Fejr88MFl0'

USERNAME = 'ESPN'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

r= twitter.get_user_timeline(screen_name= USERNAME)

for x in r:
	y = {}
	y['_id'] = x['id_str']
	y['class'] = USERNAME
	y['text'] = x['text']
	db.tweets.save(y)


