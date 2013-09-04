# decisionTree.py ################################
"""
Script description
"""
#

# Defines and imports ######
from sklearn import tree
import textMining

dictFilePath = "_dictionary.dat"
trainFeaturesFilePath = "_TRAIN_features.dat"
testFeaturesFilePath = "_TEST_features.dat"
categoryList = ['sports','tech']
#


def formatTrainingExamples(dictionary,categoryList):
	inputFeaturesVectors = []
	inputLabels = []

	for i in range(len(categoryList)):
		with open(categoryList[i]+trainFeaturesFilePath,'r') as f:
			lines = f.readlines()[1:]
		for line in lines:
			tmp = [int(value) for value in line.split()]
			inputFeaturesVectors.append(tmp)
			inputLabels.append(i)
	return (inputFeaturesVectors,inputLabels)

if __name__ == '__main__':
	dictionary = textMining.readDictionaryFromFile("whole"+dictFilePath)
	k = formatTrainingExamples(dictionary,categoryList)
	
	#clf = tree.DecisionTreeClassifier()
	#clf = clf.fit(k[0],k[1])