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

# buildDictionary() creates the dictionary from the <nWords> most frequent tokens of the tweets from a given <category>
# Also saves the dictionary to a file
# if <nWords> is empty, nWords = None => gets all tokens
# in: nWords = int, category = str
# out: FreqDist()
def buildCategoryDictionary(category,nWords=None):
    tweetList = twitter_test.get_tweets_text(classn=category)
    freq = FreqDist()
    tmpDict = FreqDist()
    for tweet in tweetList:
        freq.update(word for word in tokenizeTweet(tweet))
    if nWords != None:
        i = 0
        for (token,frequency) in freq.iteritems():
            tmpDict[token] = frequency
            i+=1
            if i == nWords:
                break
    else:
        tmpDict = freq
    saveDictionaryToFile(tmpDict,category+categoryDictFilePath)
    return tmpDict

# updateCategoryDictionary() download new tweets from the server and update the dictionary saved earlier
# if there isn't a dictionary file, the function creates the dictionary
# parameters and the return value is the same of buildCategoryDictionary()
def updateCategoryDictionary(category,nWords=None):
    tweetList = twitter_test.get_new_tweets(classn=category)
    freq = FreqDist()
    tmpDict = FreqDist()

    for tweet in tweetList:
        freq.update(word for word in tokenizeTweet(tweet))

    try:
        oldDict = readDictionaryFromFile(category+categoryDictFilePath)
    except:
        newDict = buildCategoryDictionary(category,nWords)
        return newDict

    oldDict.update(freq)
    if nWords != None:
        i = 0
        for (token,frequency) in oldDict.iteritems():
            tmpDict[token] = frequency
            i+=1
            if i == nWords:
                break
    else:
        tmpDict = oldDict
    saveDictionaryToFile(tmpDict,category+categoryDictFilePath)
    return tmpDict

# buildWholeDictionary() combines the dictionaries of every category in categoryList
# in: categoryList = list(str), nWords = int
# out: FreqDist
def buildWholeDictionary(categoryList,nWords=None):
    dictList= FreqDist()
    for category in categoryList:
        tmpDict = updateCategoryDictionary(category,nWords)
        dictList.update(tmpDict)
    saveDictionaryToFile(dictList,'whole'+categoryDictFilePath)
    return dictList

# saveDictionaryToFile() saves a dictionary into a file, one token in each line
# in: dictionary = FreqDist, dictFilePath = str
# out: None
def saveDictionaryToFile(dictionary, dictFilePath):
    with open(dictFilePath, "w") as f:
        for token in dictionary:
            f.write(token + " " + str(dictionary[token]) + "\n")

# readDictionaryFromFile() reads the <dictFilePath> file and saves the tokens into a set
# in: dictFilePath = srt
# out: dictionary = FreqDist
def readDictionaryFromFile(dictFilePath):
    dictionary = FreqDist()
    with open(dictFilePath, "r") as f:
        lines = f.readlines()
    for line in lines:
        tmp = line.strip().split()
        dictionary[tmp[0]] = int(tmp[1])
    return dictionary

# extractFeaturesFromTweet() extracts the features of a given tweet using the dictionary
# in: dictionary = FreqDist, tweet = str, category = str
# out: features = list(str) with the tokens that appear in tweet
def extractFeaturesFromTweet(dictionary, tweet, category):
    tokens = tokenizeTweet(tweet)
    features = []
    for eachToken in tokens:
        if eachToken in dictionary:
            features.append(eachToken)
    return features

# extractFeaturesFromAllTweets() extracts the features from all the tweets of categoryList
# saving them to a file, where each line represents the tokens/features activated of a example
def extractFeaturesFromAllTweets(dictionary, categoryList):
    classFeatures = []
    for category in categoryList:
        tmpList = []
        tweetList = twitter_test.get_tweets_text(classn=category)
        for tweet in tweetList:
            tmpList.append(extractFeaturesFromTweet(dictionary,tweet,category))
        classFeatures.append((tmpList,category))
    
    for (tweetFeaturesList, category) in classFeatures:
        with open(category+'_features.txt','w') as f:
            f.write(str(len(tweetFeaturesList)) + "\n")
            for tweetFeatures in tweetFeaturesList:
                for feature in tweetFeatures:
                    f.write(feature+" ")
                f.write("\n")
    
if __name__ == '__main__':
   #dictionary = updateCategoryDictionary('sports',5000)
   #extractFeaturesFromAllTweets(dictionary,['sports'])
   #dictionary = updateCategoryDictionary('tech',1000)
   dictionary = buildWholeDictionary(categoryList,2500)
   extractFeaturesFromAllTweets(dictionary,categoryList)
   #dictionary = buildWholeDictionary(categoryList,100)
   #print dictionary
   #dictionary = readDictionaryFromFile("sports_dictionary.txt")