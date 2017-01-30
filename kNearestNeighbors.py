import math
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from scipy.spatial import distance

class KNearestNeighbors():

    def __init__(self, data, labels, allLabels, k):
        self.data = data
        self.labels = labels
        self.allLabels = allLabels
        self.k = k
        
    def classify(self, newMember):
        distances = []
        neighbors = []
        for x in self.data:
            distances.append(distance.euclidean(x, newMember))

        tempLabels = []
        nieghbors = []
        for label in self.labels:
            tempLabels.append(label)
            
        for y in range(self.k):
            minIndex = distances.index(min(distances))
            neighbors.append(tempLabels[minIndex])
            tempLabels.pop(minIndex)
            distances.pop(minIndex)

        counts = []
        for label in self.allLabels:
            counts.append(neighbors.count(label))
        classification = self.allLabels[counts.index(max(counts))]
        return classification
    
    def classifyGroup(self, group):
        classifications = []
        for member in group:
            classifications.append(self.classify(member))
        return classifications
    
    def scoreTest(self, group, answers):
        guesses = self.classifyGroup(group)
        score = 0
        for i, guess in enumerate(guesses):
            if guess == answers[i]:
                score += 1

        return score / float(len(guesses))


if __name__ == "__main__":
    irisData = datasets.load_iris()
    Xset,Xtest, Yset, Ytest = train_test_split(irisData.data, irisData.target, test_size = .75)
    labels = []
    for y in Yset:
        if y not in labels:
            labels.append(y)
    clf = KNearestNeighbors(Xset, Yset, labels, 5)
    print(clf.scoreTest(Xtest, Ytest))
