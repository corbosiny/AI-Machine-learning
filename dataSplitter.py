import math
import random

class DataSplitter():

    def createTestTrainingSplit(sampleData, trainRatio= .5):
        numTrainingPoints = math.ceil(len(sampleData) * trainRatio)
        numTestingPoints = math.floor(len(sampleData) * round((1 - trainRatio), 3))
        trainingData = random.sample(sampleData, numTrainingPoints)
        sampleData = [x for x in sampleData if x not in trainingData]
        testingData = random.sample(sampleData, numTestingPoints)
        return trainingData, testingData
    
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

    print("OriginalSet: ", [i for i in range(1,11)])
    print("\n")
    for i in range(1, 11):
        trainingSet, testingSet = DataSplitter.createOrdered5TestTrainingSplit(nums, i / 10.0)
        print("Ratio: ", i / 10.0)
        print("TrainingSet: ", trainingSet)
        print("TestingSet: ", testingSet)
        print("\n")
    
