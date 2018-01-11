import random

def randomRule(trainingData, testingData):
    labels = [dataPoint[-1] for dataPoint in trainingData]
    uniqueLabels = list(set(labels))

    predictions = []
    for prediction in range(len(testingData)):
        labelNum = random.randrange(len(uniqueLabels))
        predictions.append(labels[labelNum])
    
    return predictions



def zeroRule(trainingData, testingData):
    labels = [dataPoint[-1] for dataPoint in trainingData]
    uniqueLabels = list(set(labels))
    counts = {label : labels.count(label) for label in uniqueLabels}

    maxLabel = None
    maxCount = 0
    for label in counts:
        if counts[label] > maxCount:
            maxLabel = label
            maxCount = counts[label]

    return [maxLabel for dataPoint in testingData]


def zeroRuleRegression(trainingData, testingData):
    outputs = [dataPoint[-1] for dataPoint in trainingData]
    mean = sum(outputs) / len(outputs)
    predictions = [mean for dataPoint in testingData]
    return predictions


def confusionMatrix(actual, predicted):
    pass
    

if __name__ == "__main__":
    trainingSet = [[0, 2, 'Green'], [1, 4, 'Red'], [5, 2, 'Yellow'], [1, 1, 'Green'], [0, 0, 'Blue']]
    testingSet = [[1,1], [3,2], [4,5], [7,1], [3,2]]

    print("Random Rule: ", randomRule(trainingSet, testingSet))
    print("Zero Rule: ", zeroRule(trainingSet, testingSet))

    trainRegressionSet = [[2,3,4], [1,1,5], [2,3,6], [1,2,7]]
    testRegressionSet = [[], [], []]
    print("Zero Regression Rule: ", zeroRuleRegression(trainRegressionSet, testRegressionSet))
