# decisionTree.py ################################
"""
Script description
"""
#

# Defines and imports ######
from sklearn import tree
import textMining.py

dictFilePath = "_dictionary.txt"
trainFeaturesFilePath = "_TRAIN_features.txt"
categoryList = ['sports','tech']
#


def formatInputExamples(dictionary,categoryList):
	pass

if __name__ == '__main__':
	dictionary = readDictionaryFromFile("whole"+dictFilePath)
	k = formatInputExamples(dictionary,categoryList)