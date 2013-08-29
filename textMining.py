""" Script de text mining """
import twitter_test
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem.snowball import EnglishStemmer
from Queue import Queue
import threading
import string


categoryList = ['sport']
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
q_token = Queue()
q_freq = Queue()

def freq_update(freq):
    while True:
        tokens = q_freq.get()
       # print tokens
        freq.update(word for word in tokens)
        q_freq.task_done()



def tokenizeTweet():
    while True:

        tweet = q_token.get()
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

        q_freq.put(tokens)
        q_token.task_done()

# buildDictionary() creates the dictionary from the <nWords> most frequently tokens of the tweets from a given <category>
# if <nWords> is empty, nWords = None
# in: nWords = int
# out: set()
def buildCategoryDictionary(category='',nWords=None):
    tweetList = twitter_test.get_tweets_text(classn=category)
    freq = FreqDist()

    for i in range(2):
        t = threading.Thread(target=tokenizeTweet)
        t.setDaemon(True)
        t.start()
    
    for tweet in tweetList:
        q_token.put(tweet)

    for i in range(10):
        t = threading.Thread(target=freq_update, args=(freq,))
        t.setDaemon(True)
        t.start()

    q_token.join()
    print 'waiting for freq to update ..'
    q_freq.join()

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
   
    dictionary = buildWholeDictionary(objCategory,restCategory,100)
    saveDictionaryToFile(dictionary, "dict.txt")
   # dictionary = readDictionaryFromFile("dict.txt")
   # print dictionary
   # print 'great' in dictionary
