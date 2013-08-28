""" Script de text mining """
#import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer
import string

tweet = "Arsenal's got their swagger back. The Gunners just qualified for the Champions League Group Stage for the 16th straight year. #victory"


# tokenizeTweet(tweet) receives a string representing the tweet and parses it 
# into tokens, stemming them as possible.
# in: tweet = str
# out: list[str]

# Note: it does not consider hashtags. '#bla' is treated as 'bla'
def tokenizeTweet(tweet):
	allWords = [word.lower() for sentence in sent_tokenize(tweet) for word in word_tokenize(sentence)]
	possibleWords = filter(lambda x: x not in stopwords.words('english') and x not in string.punctuation, allWords)
	
	stemmer = EnglishStemmer()
	tokens = []
	for word in possibleWords:
		tokens.append(str(stemmer.stem(word)))
	return tokens

if __name__ == '__main__':
	print tokenizeTweet(tweet)


