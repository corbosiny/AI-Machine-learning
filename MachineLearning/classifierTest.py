import numpy
import random
import warnings
warnings.filterwarnings("ignore")

#importing all our classifiers
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from kNearestNeighbors import KNearestNeighbors
import kMeans
from kNearestNeighbors import KNearestNeighbors
from sklearn.neighbors import KNeighborsClassifier

##doing a comparison test of my alogrithms to scikit-learn's for fun!
##The data used is real cancer data publicly available data from their website, it needs a tiny bit of wrangling to organize
##Run the code to see how well each of the classifiers are working!
def dataSplit(inputs, labels, testPercentage = .5): #splits a data set into a training and test set
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
    for i in range(len(lines)):    #doing a bit of data wrangling here to seperate out inputs and labels of the data
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
                inputs.pop(i) #cleaning out bad data
                labels.pop(i)
                con += 1
                break
            
    
    inputs, labels, testData, testLabels = dataSplit(inputs, labels, .20)

    #training up our models/classifiers
    clfTree = tree.DecisionTreeClassifier()
    clfNeighbors = KNearestNeighbors(inputs, labels)
    clfMeans = kMeans.KMeans(inputs, labels)
    clfGaussian = GaussianNB()
    clfSVM = svm.SVC()
    clfNeigh = KNeighborsClassifier(algorithm= 'auto', n_neighbors = 3).fit(inputs, labels)

    clfTree = clfTree.fit(inputs, labels)
    clfGaussian = clfGaussian.fit(inputs, labels)
    clfMeans.fit()
    clfSVM.fit(inputs, labels)
    
    #and heres where we do the comparison test
    print("Sklearn Classifiers:")
    print("Nearest Neighbors: ", clfNeigh.score(testData, testLabels))
    print("K-means: ", "Kmeans from sklearn can't classify data, mine can")
    print('-' * 25)
    print("My classifiers: ")
    print("K-Nearest Neighbors: ", clfNeighbors.scoreTest(testData, testLabels))
    print("K-Means: ", clfMeans.scoreTest(testData, testLabels))
    
    print('-' * 25)
    print("Extra Classifiers for fun:")
    print("Desicion Tree: ", clfTree.score(testData, testLabels))
    print("Naive Bayes: ", clfGaussian.score(testData, testLabels))
    print("SVM: ", clfSVM.score(testData, testLabels))

