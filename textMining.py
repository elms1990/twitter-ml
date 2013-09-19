# textMining.py ################################
"""
Script responsible for all the functions related to text mining:
Splitting a tweet into tokens
"""
# Defines and imports ######
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer
from string import punctuation

ourStopWords = [
    "'s", "n't", "''", "...", "``", "gt", "lt", "quot", "amp", "oelig", "scaron", "tilde", "ensp", "emsp",
    "zwnj", "zwj", "lrm", "rlm", "ndash", "mdash", "ldquo", "rdquo", "lsquo", "rsquo", "sbquo", "bdquo", "lsaquo", "rsaquo", "--"]
ourStopWords += stopwords.words('english') + list(punctuation)
ourStopWords = set(ourStopWords)

# tokenizeTweet(tweet) receives a string representing the tweet and parses it into tokens
# stemming them as possible. Discard @users and urls but saves #hashtags
# in: tweet = str
# out: list[str]
def tokenizeTweet(tweet,unique = True):
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
		aux = str(stemmer.stem(word))
		if unique:
			if(aux not in tokens):		# this makes each token appears only once
				tokens.append(aux)
		else:
			tokens.append(aux)			
	for tag in hashtags:		# this makes each token appears only once
		if unique:
			if '#' + tag not in tokens:
				tokens.append('#' + tag)
		else:
			tokens.append('#'+tag)
	return tokens

if __name__ == '__main__':
	pass
