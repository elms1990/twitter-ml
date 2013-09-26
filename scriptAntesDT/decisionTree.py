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

trainGroupSize = 5000
testGroupSize = 1000
nFeatures = 1000
########


def formatExamples(categoryList, nExamples, flagTrainTest):
    inputFeaturesVectors = np.ndarray(shape=(nExamples,nFeatures),dtype=np.float32)
    inputLabels = np.ndarray(shape=(nFeatures),dtype=np.float64)
    for i in range(len(categoryList)):
        with open(categoryList[i] + "_" + flagTrainTest + FeaturesFilePath, 'r') as f:
            fileLines = f.readlines()
        examplesFeatures = sample(fileLines, nExamples)
        for featureVector in examplesFeatures:
            tmp = [np.float32(value) for value in featureVector.split()]
            inputFeaturesVectors = np.append(inputFeaturesVectors,np.ndarray(tmp))
            inputLabels = np.append(inputLabels,np.ndarray([np.float64(i)]))
            #inputFeaturesVectors.append(np.asarray(tmp, dtype=np.float32))
            #inputLabels.append(i)
    return (inputFeaturesVectors, inputLabels)


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
    train = formatExamples(categoryList, trainGroupSize, "TRAIN")
    test = formatExamples(categoryList, testGroupSize, "TEST")
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(train[0], train[1])
    result = clf.predict(test[0])
    
    print "# of examples in Train: ", str(2*trainGroupSize)
    print "# of examples in Test: ", str(2*testGroupSize)

    analyseClassification(result.tolist(), test[1].tolist())
    #print result
    #print test[1]