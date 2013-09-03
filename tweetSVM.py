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





	"""How to use
<line> .=. <target> <feature>:<value> <feature>:<value> ... <feature>:<value> # <info>
<target> .=. +1 | -1 | 0 | <float> 
<feature> .=. <integer> | "qid"
<value> .=. <float>
<info> .=. <string>
The target value and each of the feature/value pairs are separated by a space character. Feature/value pairs MUST be ordered by increasing feature number. Features with value zero can be skipped. The string <info> can be used to pass additional information to the kernel (e.g. non feature vector data). Check the FAQ for more details on how to implement your own kernel.

In classification mode, the target value denotes the class of the example. +1 as the target value marks a positive example, -1 a negative example respectively. So, for example, the line

-1 1:0.43 3:0.12 9284:0.2 # abcdef
"""