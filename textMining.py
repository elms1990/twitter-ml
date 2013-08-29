""" Script de text mining """
import twitter_test
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem.snowball import EnglishStemmer
import string

categoryList = ['sport','tech']
objCategory = ['sport']
restCategory = [x for x in categoryList if x not in objCategory]
ourStopWords = [
    "'s", "n't", "''", "...", "``", "gt", "lt", "quot", "amp", "oelig", "scaron", "tilde", "ensp", "emsp",
    "zwnj", "zwj", "lrm", "rlm", "ndash", "mdash", "ldquo", "rdquo", "lsquo", "rsquo", "sbquo", "bdquo", "lsaquo", "rsaquo","--"]
#ListaTweet = ["It was a great game yesterday! Kobe Bryant was a beast!!!","Kobe Bryant was awesome in yesterday's game! GO LAKERS", "Go Lakers, go lakers!"]

# tokenizeTweet(tweet) receives a string representing the tweet and parses it into tokens
# stemming them as possible. Discard @users and urls but saves #hashtags
# in: tweet = str
# out: list[str]


def tokenizeTweet(tweet):
    allWords = [word.lower() for sentence in sent_tokenize(tweet)
                for word in word_tokenize(sentence)]

    # deletes @users, RT and URLs and saves #hashtags
    nWords, i = len(allWords), 0
    hashtags = []
    while i < nWords:
        if allWords[i] == '@':      # @users
            allWords[i:i + 2] = []
            nWords -= 2
        elif allWords[i] == 'rt':   # delete RT
            allWords[i:i + 1] = []
            nWords -= 1
        elif allWords[i] == '#':    # save the hashtag
            try:
                hashtags.append(allWords[i + 1])
                allWords[i:i + 2] = []
                nWords -= 2
            except:
                allWords[i:i + 1] = []
                nWords -= 1
        elif allWords[i] == "http":     # delete url starting with http:
            allWords[i:i + 3] = []
            nWords -= 3
        elif allWords[i][0:3] == 'www':  # delete urls starting with www.
            allWords[i:i + 1] = []
            nWords -= 1
        else:
            i += 1

    possibleWords = filter(lambda x: x not in stopwords.words(
        'english') and x not in string.punctuation and x not in ourStopWords and x.isdigit() == False, allWords)

    stemmer = EnglishStemmer()
    tokens = []
    for word in possibleWords:
        tokens.append(str(stemmer.stem(word)))
    for tag in hashtags:
        tokens.append('#' + tag)
    return tokens

# buildDictionary() creates the dictionary from the <nWords> most frequently tokens of the tweets from a given <category>
# if <nWords> is empty, nWords = None
# in: nWords = int
# out: set()
def buildCategoryDictionary(category='',nWords=None):
    tweetList = twitter_test.get_tweets_text(classn=category)
    freq = FreqDist()

    for tweet in tweetList:
        freq.update(word for word in tokenizeTweet(tweet))

    print freq.keys()[:10]
    print freq.values()[:10]

    dictionary = set(freq.keys()[:nWords])
    return dictionary

def buildWholeDictionary(mainCategoryList,secCategoriList,nWords=None):
    dictionary = set()
    for category in mainCategoryList + secCategoriList:
        dictionary = dictionary.union(buildCategoryDictionary(category,nWords))
    return dictionary

# saveDictionaryToFile() saves a dictionary into a file, one token in each line
# in: dictionary = set(str), dictFilePath = str
# out: None
def saveDictionaryToFile(dictionary, dictFilePath):
    with open(dictFilePath, "w") as f:
        for token in dictionary:
            f.write(token + "\n")

# readDictionaryFromFile() reads the <dictFilePath> file and saves the tokens into a set
# in: dictFilePath = srt
# out: dictionary = set(str)
def readDictionaryFromFile(dictFilePath):
    with open(dictFilePath, "r") as f:
        lines = f.readlines()
    dictionary = set(tokens.strip() for tokens in lines)
    return dictionary


def describeFeaturesFromTweet(dictionary, tweet):

    pass

if __name__ == '__main__':
    #dictionary = buildCategoryDictionary('tech', 100)
    dictionary = buildWholeDictionary(objCategory,restCategory,100)
    saveDictionaryToFile(dictionary, "dict.txt")
   # dictionary = readDictionaryFromFile("dict.txt")
    # print dictionary
    # print 'great' in dictionary
