import math
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from scipy.spatial import distance

class KNearestNeighbors():

    def __init__(self, data, labels, allLabels, k): #needs its training set and labels, then a list of all possible labels, and the number of neighbours
        self.data = data
        self.labels = labels
        self.allLabels = allLabels
        self.k = k
        
    def classify(self, newMember):      #returns a prediction of what the new member should be classified as
        distances = []
        neighbors = []
        for x in self.data:
            distances.append(distance.euclidean(x, newMember)) #essentially sums the difference squared between each attriubte of newMember and existing member in the data

        tempLabels = []
        nieghbors = []  #creates a temporary list of all the training set, so we can manipulate it without changing the actual set
        for label in self.labels:
            tempLabels.append(label)
            
        for y in range(self.k): #find the nearest neighbor, then remove him from the list and keep track of what his classification is
            minIndex = distances.index(min(distances))
            neighbors.append(tempLabels[minIndex])
            tempLabels.pop(minIndex)
            distances.pop(minIndex)

        counts = [] #here we count how many times he each label appears in the closest neighbors, the one with the most counts wins
        for label in self.allLabels:
            counts.append(neighbors.count(label))
        classification = self.allLabels[counts.index(max(counts))]
        return classification
    
    def classifyGroup(self, group): #essentially predicts classifications for a whole group of data, passes each one through the classify function
        classifications = []
        for member in group:
            classifications.append(self.classify(member))
        return classifications
    
    def scoreTest(self, group, answers):   #classifies a group then checks its scores against the answers, used for testing
        guesses = self.classifyGroup(group)
        score = 0
        for i, guess in enumerate(guesses):
            if guess == answers[i]:
                score += 1

        return score / float(len(guesses))


if __name__ == "__main__":
    #below is just test code
    irisData = datasets.load_iris() #load in the iris data set
    Xset,Xtest, Yset, Ytest = train_test_split(irisData.data, irisData.target, test_size = .75) #split it into a training set plus labels and a testing set plus labels
    labels = []
    for y in Yset: #here we calculate all possible classifications
        if y not in labels:
            labels.append(y)
    clf = KNearestNeighbors(Xset, Yset, labels, 5)
    print(clf.scoreTest(Xtest, Ytest))
