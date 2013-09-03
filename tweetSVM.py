############################# tweetSVM.py ################################
""" 
Script responsible for all the functions related to svm classification
It uses somethings from the script svmlight.py from Clint Burfoot
"""
#############################################################################

#### Defines and imports ######
import svmlight.py

categoryList = ['sports','tech']
dictionaryFile = "whole_dictionary.txt"
featuresFilePath = "_features.txt"
#############################################################################

# createExampleFile() gets every tweet/vector of features from the features files
# and writes them to the file that is going to be used by svm_learn
# IN: dictionary = FreqDist, categoryList = [str]
# OUT: nothing
def createExampleFile():
	pass


if __name__ == '__main__':
	pass