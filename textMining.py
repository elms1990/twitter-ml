""" Script de text mining """
import twitter_test
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer
import string

category = 'sport'

# tokenizeTweet(tweet) receives a string representing the tweet and parses it into tokens
# stemming them as possible. Discard @users and urls but saves #hashtags 
# in: tweet = str
# out: list[str]
def tokenizeTweet(tweet):
    allWords = [word.lower() for sentence in sent_tokenize(tweet)
                for word in word_tokenize(sentence)]

    #deletes @users, RT and URLs and saves #hashtags
    nWords, i = len(allWords), 0
    hashtags = []
    while i < nWords:
        if allWords[i] == '@':      # @users
            allWords[i:i+2] = []
            nWords-=2
        elif allWords[i] == 'rt':   # delete RT
            allWords[i:i+1] = []
            nWords-=1
        elif allWords[i] == '#':    # save the hashtag
            try:
                hashtags.append(allWords[i+1])
                allWords[i:i+2] = []
                nWords-=2
            except:
                allWords[i:i+1] = []
                nWords-=1
        elif allWords[i] == "http":     # delete url starting with http:
            allWords[i:i+3] = []
            nWords-=3
        elif allWords[i][0:3] == 'www': # delete urls starting with www.
            allWords[i:i+1] = []
            nWords-=1
        else:
            i+=1

    possibleWords = filter(lambda x: x not in stopwords.words(
        'english') and x not in string.punctuation and x.isdigit() == False, allWords)

    stemmer = EnglishStemmer()
    tokens = []
    for word in possibleWords:
        tokens.append(str(stemmer.stem(word)))
    for tag in hashtags:
        tokens.append('#'+tag)
    return tokens

# buildDictionary() creates the dictionary from the tokens of each tweet from a given <category>
# if <category> is empty, creates the dictionary from all tweets
# in: category = str
# out: set()
def buildDictionary(category):
    tweetList = twitter_test.get_tweets_text(classn=category)
    dictionary = set()
    for tweet in tweetList:
        dictionary = dictionary.union(set(tokenizeTweet(tweet)))
    return dictionary


if __name__ == '__main__':
    dictonary = buildDictionary(category)
    print len(dictonary)


   