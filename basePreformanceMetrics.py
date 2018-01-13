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
    uniqueLabels = set(actual)
    numericalValueOfLabels = {label : i for i, label in enumerate(uniqueLabels)}

    confusionMatrix = [[0 for x in range(len(uniqueLabels))] for x in range(len(uniqueLabels))] #making an n^2 matrix
    for entryNum in range(len(actual)):
        actualValue = numericalValueOfLabels[actual[entryNum]]
        predictedValue = numericalValueOfLabels[predicted[entryNum]]
        confusionMatrix[actualValue][predictedValue] += 1
            
    return uniqueLabels, confusionMatrix

def maeError(actual, predicted):
    totalError = 0
    for i in range(len(actual)):
        totalError += abs(predicted[i] - actual[i])
        return totalError / float(len(actual))

def rmsError(actual, predicted):
    totalError = 0
    for i in range(len(actual)):
        totalError += (predicted[i] - actual[i]) ** 2
        return totalError / float(len(actual))



if __name__ == "__main__":
    trainingSet = [[0, 2, 'Green'], [1, 4, 'Red'], [5, 2, 'Yellow'], [1, 1, 'Green'], [0, 0, 'Blue']]
    testingSet = [[1,1], [3,2], [4,5], [7,1], [3,2]]

    print("Random Rule: ", randomRule(trainingSet, testingSet))
    print("Zero Rule: ", zeroRule(trainingSet, testingSet))

    trainRegressionSet = [[2,3,4], [1,1,5], [2,3,6], [1,2,7]]
    testRegressionSet = [[], [], []]
    print("Zero Regression Rule: ", zeroRuleRegression(trainRegressionSet, testRegressionSet))

    actual = [0,0,0,0,0,1,1,1,1,1]
    predicted = [0,1,1,0,0,1,0,1,1,1]
    uniqueLabels, confusionMatrix = confusionMatrix(actual, predicted)
    print(confusionMatrix)
