""" Script de text mining """
import twitter_test
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem.snowball import EnglishStemmer
import string

categoryList = ['sports','tech']
ourStopWords = [
    "'s", "n't", "''", "...", "``", "gt", "lt", "quot", "amp", "oelig", "scaron", "tilde", "ensp", "emsp",
    "zwnj", "zwj", "lrm", "rlm", "ndash", "mdash", "ldquo", "rdquo", "lsquo", "rsquo", "sbquo", "bdquo", "lsaquo", "rsaquo","--"]
ourStopWords+= stopwords.words('english') + list(string.punctuation)
ourStopWords = set(ourStopWords)
#ListaTweet = ["It was a great game yesterday! Kobe Bryant was a beast!!!","Kobe Bryant was awesome in yesterday's game! GO LAKERS", "Go Lakers, go lakers!"]

categoryDictFilePath = "_dictionary.txt"

# tokenizeTweet(tweet) receives a string representing the tweet and parses it into tokens
# stemming them as possible. Discard @users and urls but saves #hashtags
# in: tweet = str
# out: list[str]


def tokenizeTweet(tweet):
    allWords = [word.lower() for word in word_tokenize(tweet)]

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

    possibleWords = filter(lambda x: x not in ourStopWords and x.isdigit() == False, allWords)

    stemmer = EnglishStemmer()
    tokens = []
    for word in possibleWords:
        tokens.append(str(stemmer.stem(word)))
    for tag in hashtags:
        tokens.append('#' + tag)
    return tokens

# buildDictionary() creates the dictionary from the <nWords> most frequently tokens of the tweets from a given <category>
# if <nWords> is empty, nWords = None => gets all tokens
# in: nWords = int
# out: list of tuples -> [(token0,frequency0),(token1,frequency1),...]
def buildCategoryDictionary(category,nWords=None):
    tweetList = twitter_test.get_tweets_text(classn=category)
    freq = FreqDist()

    for tweet in tweetList:
        freq.update(word for word in tokenizeTweet(tweet))

    print freq.keys()[:10]
    print freq.values()[:10]

    tmpDict = freq.items()[:nWords]

    saveDictionaryToFile(tmpDict,category+categoryDictFilePath)
    return dict(tmpDict)

def buildWholeDictionary(categoryList,nWords=None):
    dictList= []
    for category in categoryList:
        tmpDict = buildCategoryDictionary(category,nWords)
        #tmpDict = readDictionaryFromFile(category+categoryDictFilePath)
        dictList.append(tmpDict.items())
    return dictList

# saveDictionaryToFile() saves a dictionary into a file, one token in each line
# in: dictionary = set(str), dictFilePath = str
# out: None
def saveDictionaryToFile(dictionary, dictFilePath):
    with open(dictFilePath, "w") as f:
        for (token,freq) in dictionary:
            f.write(token + " " + str(freq) + "\n")

# readDictionaryFromFile() reads the <dictFilePath> file and saves the tokens into a set
# in: dictFilePath = srt
# out: dictionary = set(str)
def readDictionaryFromFile(dictFilePath):
    dictionary = {}
    with open(dictFilePath, "r") as f:
        lines = f.readlines()
    for line in lines:
        tmp = line.strip().split()
        dictionary[tmp[0]] = int(tmp[1])
    return dictionary

# extractFeaturesFromTweet() extracts the features of a given tweet using the dictionary
# in: dictionary = set(), tweet = str
# out: features = dictionary where features[token] = True if token appears in tweet
def extractFeaturesFromTweet(dictionary, tweet, category):
    tokens = tokenizeTweet(tweet)
    features = {}
    for eachToken in tokens:
        if eachToken in dictionary:
            features[eachToken] = True
    features['class'] = category
    return features

def extractFeaturesFromAllTweets(dictionary, mainCategoryList,secCategoriList):
    mainClassFeatures = []
    secClassFeatures = []
    for category in mainCategoryList:
        tweetList = twitter_test.get_tweets_text(classn=category)
        for tweet in tweetList:
            mainClassFeatures.append(extractFeaturesFromTweet(dictionary,tweet,category))
    for category in secCategoryList:
        tweetList = twitter_test.get_tweets_text(classn=category)
        for tweet in tweetList:
            secClassFeatures.append(extractFeaturesFromTweet(dictionary,tweet,category))

    """ IMPLEMENTAR O qUE faZER COM A LISTA DOS FEATURES: 
        ESCREVER NUM ArQUIVO, OU GUARdar NO banCO de dados
    """
    
if __name__ == '__main__':
   #dictionary = buildCategoryDictionary('tech', 100)
   # dictionary = buildWholeDictionary(objCategory,restCategory,100)
   dictionary = buildWholeDictionary(categoryList,100)
   print dictionary