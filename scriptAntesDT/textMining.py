# textMining.py ################################
"""
Script responsible for all the functions related to text mining:
Splitting a tweet into tokens, creating and updating the dictionaries and
extracting the features of a tweet given a dictionary
"""
#

# Defines and imports ######
import twitter_fetch
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem.snowball import EnglishStemmer
from string import punctuation
from math import ceil
from random import sample

categoryList = ['sports', 'tech']
ourStopWords = [
    "'s", "n't", "''", "...", "``", "gt", "lt", "quot", "amp", "oelig", "scaron", "tilde", "ensp", "emsp",
    "zwnj", "zwj", "lrm", "rlm", "ndash", "mdash", "ldquo", "rdquo", "lsquo", "rsquo", "sbquo", "bdquo", "lsaquo", "rsaquo", "--"]
ourStopWords += stopwords.words('english') + list(punctuation)
ourStopWords = set(ourStopWords)

categoryDictFilePath = "_dictionary.dat"
freqPercentage = 0.9
nonFreqPercentage = 0.1
#

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

    possibleWords = filter(
        lambda x: x not in ourStopWords and x.isdigit() == False, allWords)

    stemmer = EnglishStemmer()
    tokens = []
    for word in possibleWords:
        tokens.append(str(stemmer.stem(word)))
    for tag in hashtags:
        tokens.append('#' + tag)
    return tokens

# buildDictionary() creates the dictionary from the tokens of the tweets from a given <category>
# Also saves the dictionary to a file
# in: category = str
# out: FreqDist()
def buildCategoryDictionary(category):
    tweetList = twitter_fetch.get_tweets_text(classn=category)
    freq = FreqDist()
    for tweet in tweetList:
        freq.update(word for word in tokenizeTweet(tweet))
    saveDictionaryToFile(freq, category + categoryDictFilePath)
    return freq

# updateCategoryDictionary() download new tweets from the server and update the dictionary saved earlier
# if there isn't a dictionary file, the function creates the dictionary
# parameters and the return value is the same of buildCategoryDictionary()
def updateCategoryDictionary(category):
    tweetList = twitter_fetch.get_new_tweets(classn=category)
    freq = FreqDist()
    tmpDict = FreqDist()

    for tweet in tweetList:
        freq.update(word for word in tokenizeTweet(tweet))

    try:
        oldDict = readDictionaryFromFile(category + categoryDictFilePath)
    except:
        newDict = buildCategoryDictionary(category)
        return newDict

    oldDict.update(freq)
    saveDictionaryToFile(oldDict, category + categoryDictFilePath)
    return oldDict

# buildWholeDictionary() combines the dictionaries of every category in categoryList
# in: categoryList = list(str), nWords = int
# out: [str] = list of the tokens from the dictionary
def buildWholeDictionary(categoryList, nWords):
    dictList = []
    for category in categoryList:
        tmpDict = updateCategoryDictionary(category)
        #tmpDict = buildCategoryDictionary(category)
        dictList.append(tmpDict)
    wholeDictionary = selectNWordsFromDict(dictList, nWords)
    saveDictionaryToFile(wholeDictionary, 'whole' + categoryDictFilePath)
    return wholeDictionary.keys()

# selectNWordsFromDict() receives the FreqDists of each category and samples nWords from it
# The size of the resultant dictionary is smaller than nWords
# in: dictList = [FreqDist,...], nWords = int
# out: FreqDist()
def selectNWordsFromDict(dictList, nWords):
    wordPerCategory = nWords / len(dictList)
    freqWords = int(ceil(wordPerCategory * freqPercentage))
    nonFreqWords = int(ceil(wordPerCategory * nonFreqPercentage))

    wholeDictionary = []

    print "Selecting ", nWords, " words for the big dictionary"
    print wordPerCategory, " words per category"
    print freqWords, " frequent words"
    print nonFreqWords, " non frequent words"

    for catDict in dictList:
        keys = catDict.keys()
        print keys[:freqWords]
        wholeDictionary += keys[:freqWords]
        wholeDictionary += sample(keys[freqWords:], nonFreqWords)

    return FreqDist(wholeDictionary)  #returns a FreqDist just because it is easier to save it to a file

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
# in: dictionary = FreqDist/list(str), tweet = str, category = str
# out: features = list(str) with the tokens that appear in tweet
# out2: features = list(0,1) where 1 if the i-th token of the dictionary appeared in tweet. 0 otherwise


def extractFeaturesFromTweet(dictionary, tweet, category):
    tokens = tokenizeTweet(tweet)
    features = []
    # First way of doing it
    # for eachToken in tokens:
    #     if eachToken in dictionary:
    #         features.append(eachToken)

    # Another way. CAREFULL probably too big!!!
    for eachToken in dictionary:
        if eachToken in tokens:
            features.append('1')
        else:
            features.append('0')
    return features

# extractFeaturesFromAllTweets() extracts the features from all the tweets of categoryList
# saving them to a file, where each line represents the tokens/features
# activated of a example
# trainPercentage represents the % of training examples, if > 0.0 separates into train and test group

def extractFeaturesFromAllTweets(dictionary, categoryList, trainPercentage = 0.0):
    classFeatures = []
    for category in categoryList:
        tmpList = []
        tweetList = twitter_fetch.get_tweets_text(classn=category)
        for tweet in tweetList:
            tmpList.append(
                extractFeaturesFromTweet(dictionary, tweet, category))
        classFeatures.append((tmpList, category))

    if trainPercentage == 0.0:
        for (tweetFeaturesList, category) in classFeatures:
            with open(category + '_features.dat', 'w') as f:
                f.write(str(len(tweetFeaturesList)) + "\n")
                for tweetFeatures in tweetFeaturesList:
                    for feature in tweetFeatures:
                        f.write(feature + " ")
                    f.write("\n")
    else:
        for (tweetFeaturesList, category) in classFeatures:
            nTrain = int(ceil(trainPercentage*len(tweetFeaturesList)))
            nTest = len(tweetFeaturesList) - nTrain

            with open(category + '_TRAIN_features.dat', 'w') as f:
                f.write(str(nTrain) + "\n")
                for i in range(nTrain):
                    for feature in tweetFeaturesList[i]:
                        f.write(feature + " ")
                    f.write("\n")
            with open(category + '_TEST_features.dat', 'w') as f:
                f.write(str(nTest) + "\n")
                for i in range(nTest):
                    for feature in tweetFeaturesList[i+nTrain]:
                        f.write(feature + " ")
                    f.write("\n")

if __name__ == '__main__':
    #dictionary = buildWholeDictionary(categoryList, 1000)
    dictionary = readDictionaryFromFile("whole_dictionary.dat")
    extractFeaturesFromAllTweets(dictionary,categoryList,0.5)
    