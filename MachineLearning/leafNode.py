from __future__ import division

class Leaf():

    def __init__(self, data):
        self.data = data

    def predict(self):
        labels = set([point[-1] for point in self.data])

        if len(labels) == 0:
            return labels[0]
        else:
            return self.predictFromLabels(labels)

    def predictFromLabels(self, labels):
        dataLabels = [point[-1] for point in self.data]
        counts = {label : dataLabels.count(label) for label in labels}

        probabilities = {label : counts[label] / len(dataLabels) for label in labels}

        bestLabel = Leaf.findMaxLabel(probabilities)
        
        return bestLabel

    def findMaxLabel(probabilities):
        bestLabel, bestProbability = None, -1

        for label in probabilities:
            if probabilities[label] > bestProbability:
                bestLabel = label
                bestProbability = probabilities[label]

        return bestLabel


if __name__ == "__main__":
    testData = [[1, 1], [5, 1], [2, 1], [2, 1], [3, 0], [1, 0]]
    leaf = Leaf(testData)
    print(leaf.predict())
