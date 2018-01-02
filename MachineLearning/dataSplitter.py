import math
import random

class DataSplitter():

    def createTestTrainingSplit(sampleData, trainRatio= .5):
        trainingSetSize = int(len(sampleData) * trainRatio)
        trainingSet = []
        testingSet = list(sampleData)
        while len(trainingSet) < trainingSetSize:
            index = random.randrange(len(testingSet))
            trainingSet.append(testingSet.pop(index))
            
        return trainingSet, testingSet
    
    def createOrderedTestTrainingSplit(sampleData, trainRatio):
        numTrainingPoints = math.ceil(len(sampleData) * trainRatio)
        numTestingPoints = math.floor(len(sampleData) * round((1 - trainRatio), 3))

        listOfIndicies = random.sample(range(len(sampleData)), numTrainingPoints)
        trainingData = [sampleData[i] for i in sorted(listOfIndicies)]
        sampleData = [x for x in sampleData if x not in trainingData]
        listOfIndicies = random.sample(range(len(sampleData)), numTestingPoints)
        testingData = [sampleData[i] for i in sorted(listOfIndicies)]
        return trainingData, testingData
            
if __name__ == "__main__":
    nums = range(1, 11)

    trainingSet, testingSet = DataSplitter.createTestTrainingSplit(nums)
    print(trainingSet)
    print(testingSet)
    
    print("OriginalSet: ", [i for i in range(1,11)])
    print("\n")
    for i in range(1, 11):
        trainingSet, testingSet = DataSplitter.createOrderedTestTrainingSplit(nums, i / 10.0)
        print("Ratio: ", i / 10.0)
        print("TrainingSet: ", trainingSet)
        print("TestingSet: ", testingSet)
        print("\n")
    
