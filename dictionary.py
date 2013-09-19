import twitter_fetch
import textMining
from nltk.probability import FreqDist
from math import ceil
from random import sample

categoryList = ['sports', 'tech','religion']
categoryDictFilePath = "_dictionary.dat"
freqPercentage = 0.9
nonFreqPercentage = 0.1


# buildDictionary() creates the dictionary from the tokens of the tweets from a given <category>
# Also saves the dictionary to a file
# in: category = str
# out: FreqDist() that shows in how many documents each token appears
def buildCategoryDictionary(category):
    tweetList = twitter_fetch.get_tweets_text(classn=category)
    freq = FreqDist()
    for tweet in tweetList:
        freq.update(word for word in textMining.tokenizeTweet(tweet))
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
        freq.update(word for word in textMining.tokenizeTweet(tweet))

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
# out: FreqDist() of the dictionary words and the number of documents each one appears in
def buildWholeDictionary(categoryList, nWords):
    dictList = []
    for category in categoryList:
        tmpDict = updateCategoryDictionary(category)
        #tmpDict = buildCategoryDictionary(category)
        dictList.append(tmpDict)
    wholeDictionary = selectNWordsFromDict(dictList, nWords)
    saveDictionaryToFile(wholeDictionary, 'whole' + categoryDictFilePath)
    return wholeDictionary

# selectNWordsFromDict() receives the FreqDists of each category and samples nWords from it
# The size of the resultant dictionary is smaller than nWords
# in: dictList = [FreqDist,...], nWords = int
# out: FreqDist()
def selectNWordsFromDict(dictList, nWords):
    wordPerCategory = nWords / len(dictList)
    freqWords = int(ceil(wordPerCategory * freqPercentage))
    nonFreqWords = int(ceil(wordPerCategory * nonFreqPercentage))

    wholeDictionary = FreqDist()

    print "Selecting ", nWords, " words for the big dictionary"
    print wordPerCategory, " words per category"
    print freqWords, " frequent words"
    print nonFreqWords, " non frequent words"

    for catDict in dictList:
	freqTuples = catDict.items()[:freqWords]
	for eachTuple in freqTuples:
		wholeDictionary[eachTuple[0]] = wholeDictionary[eachTuple[0]] + eachTuple[1]
	nonFreqTuples = sample(catDict.items()[freqWords:],nonFreqWords) 
	for eachTuple in nonfreqTuples:
		wholeDictionary[eachTuple[0]] = wholeDictionary[eachTuple[0]] + eachTuple[1]
    return wholeDictionary

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

############### ALTERAR DAQUI PRA BAIXO ##################

# extractFeaturesFromTweet() will construct the FV using TF-IDF
# in: dictionary = FreqDist/list(str), tweet = str, category = str
def extractFeaturesFromTweet(dictionary, tweet, category):
	return

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

	    print "# tweets "+category+": "
	    print nTrain," TRAIN"
	    print nTest, " TEST"

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
