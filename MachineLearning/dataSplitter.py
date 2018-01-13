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

    def randomSubSample(dataSet, ratio = .5):
        sample = []
        copyOfDataSet = [dataPoint for dataPoint in dataSet]
        while len(sample) < round(len(dataSet) * ratio):
            index = random.randrange(len(copyOfDataSet))
            sample.append(copyOfDataSet.pop(index))

        return sample

    def kFoldsSplit(dataSet, numFolds):
        folds = []
        copyOfData = list(dataSet)_
        foldSize = int(len(dataSet) / numFolds)
        for foldNum in range(numFolds):
            fold = []
            while len(fold) < foldSize:
                index = random.randrange(len(copyOfData))
                fold.append(copyOfData.pop(index))
            folds.append(fold)

        return folds
    
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for i in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split
if __name__ == "__main__":
    nums = range(1, 11)

    trainingSet, testingSet = DataSplitter.createTestTrainingSplit(nums)
    print(trainingSet)
    print(testingSet)
    

    dataSet = [1,3,5,7,9,11]
    for i in range(3):
        print(DataSplitter.randomSubSample(dataSet))
