""" Script de text mining """
from twitter_test import get_tweets_text
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer
import string

#tweet = "RT Arsenal's got their swagger back. The Gunners just qualified qualify for the Champions League Group Stage for the 16th straight year. @nba_nbb #victory"

# tokenizeTweet(tweet) receives a string representing the tweet and parses it into tokens
# stemming them as possible. Discard @users but saves #hashtags 
# in: tweet = str
# out: list[str]

# Note: it does not consider hashtags. '#bla' is treated as 'bla', '@nba' is treated as 'nba'
def tokenizeTweet(tweet):
    allWords = [word.lower() for sentence in sent_tokenize(tweet)
                for word in word_tokenize(sentence)]

    #deletes @users and RT and saves #hashtags
    nWords, i = len(allWords), 0
    hashtags = []
    while i < nWords:
        if allWords[i] == '@':
            allWords[i:i+2] = []
            nWords-=2
        elif allWords[i] == 'rt':
            allWords[i:i+1] = []
            nWords-=1
        elif allWords[i] == '#':
            hashtags.append(allWords[i+1])
            allWords[i:i+2] = []
            nWords-=2
        else:
            i+=1

    possibleWords = filter(lambda x: x not in stopwords.words(
        'english') and x not in string.punctuation, allWords)

    stemmer = EnglishStemmer()
    tokens = []
    for word in possibleWords:
        tokens.append(str(stemmer.stem(word)))
    for tag in hashtags:
        tokens.append('#'+tag)
    return tokens

## Work In Progress
def buildDictionary():
    tweetList = [each.encode('ascii','ignore') for each in get_tweets_text()]
    print tweetList


if __name__ == '__main__':
    buildDictionary()
