import warnings
warnings.filterwarnings("ignore")

import math
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from scipy.spatial import distance


#classifies an object by the labels of its nearest datapoints
class KNearestNeighbors():

    def __init__(self, data, labels, allLabels = None, k= 3): #needs a set of datapoints, their labels, all the possible lavels, and how many neighbors to search for **note** k should be odd to avoid ties
        self.data = data
        self.labels = labels
        if allLabels:
            self.allLabels = allLabels
        else:
            allLabels = []
            for label in labels:
                if label not in allLabels:
                    allLabels.append(label)
            self.allLabels = allLabels
            
        self.k = k
        
    def predictPoint(self, newMember): 
        distances = []
        neighbors = [] 
        for x in self.data:
            distances.append(distance.euclidean(x, newMember)) #finding all the distances

        tempLabels = []
        nieghbors = []
        for label in self.labels:
            tempLabels.append(label) #making a temp array to hold all of our data labels so that we can remove some when finding nearest neighbors
            
        for y in range(self.k):                         #finding as many nearest neighbors as specified
            minIndex = distances.index(min(distances))  
            neighbors.append(tempLabels[minIndex])      #adding on the label of the nearest neighbor
            tempLabels.pop(minIndex)                    #removing that data point
            distances.pop(minIndex)

        counts = []                                     
        for label in self.allLabels:                    #going through each label and making an array that holds a list of the frequencies
            counts.append(neighbors.count(label))
        classification = self.allLabels[counts.index(max(counts))] #returning the most frequent label
        return classification
    
    def predict(self, group):         #takes a list of points, classifies them and returns an array of the classification
        classifications = []
        if isinstance(group[0], list):
            for member in group:
                classifications.append(self.predictPoint(member))
        else:
            return self.predictPoint(group)
            
        return classifications
    
    def scoreTest(self, group, answers):        #test the accuracy of the classifier, takes in a group of points, classifies them, checks that against the answers
        guesses = self.predict(group)
        score = 0
        for i, guess in enumerate(guesses):
            if guess == answers[i]:
                score += 1

        return score / float(len(guesses))


###just test code below###
if __name__ == "__main__":
    irisData = datasets.load_iris()
    Xset,Xtest, Yset, Ytest = train_test_split(irisData.data, irisData.target, test_size = .75)
    labels = []
    for y in Yset:
        if y not in labels:
            labels.append(y)
    clf = KNearestNeighbors(Xset, Yset, labels, 5)
    print(clf.scoreTest(Xtest, Ytest))
