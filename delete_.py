import nltk

from pymongo import Connection

db = Connection(
    'mongodb://test:test@paulo.mongohq.com:10063/TweetCat').TweetCat

for x in db.tweets.find():
	x['new'] = False
	db.tweets.save(x)

b =  [x for x in db.tweets.find({'user':'google'}).sort('_id',-1).limit(4)]
print b


# if __name__ == '__main__':
# 	nltk.download()