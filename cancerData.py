import numpy
import random
import warnings
from copy import deepcopy
warnings.filterwarnings("ignore")

from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from kNearestNeighbors import KNearestNeighbors
import kMeans
from kNearestNeighbors import KNearestNeighbors
from sklearn.neighbors import KNeighborsClassifier

def dataSplit(inputs, labels, testPercentage = .5):
    numLoops = len(inputs) * testPercentage

    rngState = numpy.random.get_state()
    numpy.random.shuffle(inputs)
    numpy.random.set_state(rngState)
    numpy.random.shuffle(labels)

    trainData = inputs
    testData = []

    trainLabels = labels
    testLabels = []
    
    for i in range(int(numLoops)):
        testData.append(trainData.pop(i))
        testLabels.append(trainLabels.pop(i))

    return trainData, trainLabels, testData, testLabels
        


with open('breast-cancer-wisconsin.data.txt', 'r') as file:
    lines = file.readlines()

    inputs = []
    labels = []
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n')
        inputs.append(lines[i][0:-1].split(','))
        inputs[i].pop(0)
        inputs[i].pop(-1)
        labels.append(lines[i][-1])

    con = 0
    for i in range(len(labels)):
        if con:
            i -= con

        for j in range(len(inputs[i])):
            try:
                inputs[i][j] = float(inputs[i][j])
            except:
                inputs.pop(i)
                labels.pop(i)
                con += 1
                break
            
    
    inputs, labels, testData, testLabels = dataSplit(inputs, labels, .20)

    inputs2 = deepcopy(inputs)
    inputs3 = deepcopy(inputs)

    testData2 = deepcopy(testData)
    
    clfTree = tree.DecisionTreeClassifier()
    print(inputs[0:5])
    print(inputs2[0:5])
    clfMeans = kMeans.KMeans(inputs2, labels, featureScaling = True)
    clfMeans.fit()
    clfGaussian = GaussianNB()
    clfSVM = svm.SVC()
    clfNeigh = KNeighborsClassifier(algorithm= 'auto', n_neighbors = 3).fit(inputs3, labels)
    clfNeighbors = KNearestNeighbors(inputs, labels,  featureScaling = True)

    clfTree = clfTree.fit(inputs, labels)
    clfGaussian = clfGaussian.fit(inputs, labels)
    clfSVM.fit(inputs, labels)
    print("Sklearn Classifiers:")
    print("Nearest Neighbors: ", clfNeigh.score(testData, testLabels))
    print("K-means: ", "Kmeans from sklearn can't classify labeled data")
    print('-' * 25)
    print("My classifiers: ")
    print("K-Means: ", clfMeans.scoreTest(testData2, testLabels))
    print("K-Nearest Neighbors: ", clfNeighbors.scoreTest(testData, testLabels))
    
    print('-' * 25)
    print("Extra Classifiers for fun:")
    print("Desicion Tree: ", clfTree.score(testData, testLabels))
    print("Naive Bayes: ", clfGaussian.score(testData, testLabels))
    print("SVM: ", clfSVM.score(testData, testLabels))
