# decisionTree.py ################################
"""
Script description
"""
#

# Defines and imports ######
from sklearn import tree
import textMining

dictFilePath = "_dictionary.dat"
FeaturesFilePath = "_features.dat"
categoryList = ['sports','tech']
#

#flagTrainTest = TRAIN or TEST
def formatExamples(categoryList,flagTrainTest='TRAIN'):
	inputFeaturesVectors = []
	inputLabels = []
	x = 1901
	if flagTrainTest == "TEST":
		x = 51

	for i in range(len(categoryList)):
		with open(categoryList[i]+"_"+flagTrainTest+FeaturesFilePath,'r') as f:
			lines = f.readlines()[1:x]
		for line in lines:
			tmp = [int(value) for value in line.split()]
			inputFeaturesVectors.append(tmp)
			inputLabels.append(i)
	return (inputFeaturesVectors,inputLabels)	

if __name__ == '__main__':
	#dictionary = textMining.readDictionaryFromFile("whole"+dictFilePath)
	k = formatExamples(categoryList,"TRAIN")
	j = formatExamples(categoryList,"TEST")
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(k[0],k[1])
	result = clf.predict(j[0])

	i = 0
	for m in range(len(j[1])):
		if j[1][m]==result[m]:
			i+=1
	print "Got ",str(i),"from ",str(len(j[1]))
