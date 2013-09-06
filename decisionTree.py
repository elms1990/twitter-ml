# decisionTree.py ################################
"""
Script description
"""
#

# Defines and imports ######
from sklearn import tree
from random import sample
import numpy as np
import textMining

dictFilePath = "_dictionary.dat"
FeaturesFilePath = "_features.dat"
categoryList = ['tech','sports']

trainGroupSize = 2000
testGroupSize = 100
########


def formatExamples(categoryList, nExamples, flagTrainTest):
    inputFeaturesVectors = []
    inputLabels = []
    for i in range(len(categoryList)):
        with open(categoryList[i] + "_" + flagTrainTest + FeaturesFilePath, 'r') as f:
            fileLines = f.readlines()
        examplesFeatures = sample(fileLines, nExamples)
        for featureVector in examplesFeatures:
            tmp = [int(value) for value in featureVector.split()]
            inputFeaturesVectors.append(tmp)
            inputLabels.append(i)
    return (np.array(inputFeaturesVectors), np.array(inputLabels))


def analyseClassification(resultLabels, targetLabels):
    truePositive, trueNegative = 0.0, 0.0
    falsePositive, falseNegative = 0.0, 0.0

    for i in range(len(targetLabels)):
        if targetLabels[i] == 1 and resultLabels[i] == 1:
            truePositive += 1.0
        elif targetLabels[i] == 1 and resultLabels[i] == 0:
            falseNegative += 1.0
        elif targetLabels[i] == 0 and resultLabels[i] == 1:
            falsePositive += 1.0
        elif targetLabels[i] == 0 and resultLabels[i] == 0:
            trueNegative += 1.0

    # proportion of correct predictions considering the positive and negative
    # inputs#
    accuracy = float((truePositive + trueNegative)/len(targetLabels)) * 100.0
    # the proportion of the true positives, that is, the ability of the system
    # on predicting the correct values#
    sensitivity = float(truePositive / (truePositive + falseNegative)) * 100.0
    # the ability of the system on predicting the correct values for the cases
    # that are the opposite to the desired one
    specificity = float(trueNegative / (trueNegative + falsePositive)) * 100.0
    # a good evaluator for measure the responsiveness in a overall situation
    # to the production of false positives and false negatives
    efficiency = float((sensitivity + specificity) / 2)
    # indicates the estimation of how good the system is when making a
    # positive affirmation
    ppv = float(truePositive / (truePositive + falsePositive)) * 100.0
    # estimation of how good the system is when making a negative affirmation
    npv = float(trueNegative / (trueNegative + falseNegative)) * 100.0

    print "Accuracy: ", accuracy, "%"
    print "Sensitivity: ", sensitivity, "%"
    print "Specificity: ", specificity, "%"
    print "Efficiency: ", efficiency, "%"
    print "Positive Predict Value: ", ppv, "%"
    print "Negative Predict Value: ", npv, "%"

#flagTrainTest = TRAIN or TEST
def formatExamples(categoryList,nExamples,flagTrainTest):
	inputFeaturesVectors = []
	inputLabels = []

	for i in range(len(categoryList)):
		with open(categoryList[i]+"_"+flagTrainTest+FeaturesFilePath,'r') as f:
			lines = f.readlines()[1:nExamples+1]
		for line in lines:
			tmp = [int(value) for value in line.split()]
			inputFeaturesVectors.append(tmp)
			inputLabels.append(i)
	return (inputFeaturesVectors,inputLabels)	

def analyseClassification(resultLabels, targetLabels):
    truePositive, trueNegative = 0.0, 0.0
    falsePositive, falseNegative = 0.0, 0.0

    for i in range(len(targetLabels)):
        if targetLabels[i] == 1 and resultLabels[i] == 1:
            truePositive += 1.0
        elif targetLabels[i] == 1 and resultLabels[i] == 0:
            falseNegative += 1.0
        elif targetLabels[i] == 0 and resultLabels[i] == 1:
            falsePositive += 1.0
        elif targetLabels[i] == 0 and resultLabels[i] == 0:
            trueNegative += 1.0

    # proportion of correct predictions considering the positive and negative
    # inputs#
    accuracy = float((truePositive + trueNegative)/len(targetLabels)) * 100.0
    # the proportion of the true positives, that is, the ability of the system
    # on predicting the correct values#
    sensitivity = float(truePositive / (truePositive + falseNegative)) * 100.0
    # the ability of the system on predicting the correct values for the cases
    # that are the opposite to the desired one
    specificity = float(trueNegative / (trueNegative + falsePositive)) * 100.0
    # a good evaluator for measure the responsiveness in a overall situation
    # to the production of false positives and false negatives
    efficiency = float((sensitivity + specificity) / 2)
    # indicates the estimation of how good the system is when making a
    # positive affirmation
    ppv = float(truePositive / (truePositive + falsePositive)) * 100.0
    # estimation of how good the system is when making a negative affirmation
    npv = float(trueNegative / (trueNegative + falseNegative)) * 100.0

    print "Accuracy: ", accuracy, "%"
    print "Sensitivity: ", sensitivity, "%"
    print "Specificity: ", specificity, "%"
    print "Efficiency: ", efficiency, "%"
    print "Positive Predict Value: ", ppv, "%"
    print "Negative Predict Value: ", npv, "%"

if __name__ == '__main__':
	#dictionary = textMining.readDictionaryFromFile("whole"+dictFilePath)
	k = formatExamples(categoryList,5000,"TRAIN")
	j = formatExamples(categoryList,200,"TEST")
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(k[0],k[1])
	result = clf.predict(j[0])

	analyseClassification(result,j[1])
