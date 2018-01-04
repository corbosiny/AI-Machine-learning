from naiveBayesClassifier import NaiveBayesClassifier
import random

knownDataSet = [[3, 1, 0],[4, 1, 0], [5, 1, 0], [13, 1],[14, 1],[15, 1], [20, 2], [21, 2], [23, 2]]

class NaiveBayesTester():

    def __init__(self, dataset = knownDataSet):
        self.testDataSet = dataset
        self.testClassifier = NaiveBayesClassifier(self.testDataSet)

    def test(self, datapoint = [5,2]):
        assert(self.testDataSet == self.testClassifier.trainingSet)
        
        self.testClassifier.fit()
        self.testDataSplitting()
        self.testDistributions()
        self.testPredictions()
        print("test passed!")
        
    def testDataSplitting(self):
        for label in self.testClassifier.dataSplitByClass:
            dataOfSpecificLabel = [datapoint for datapoint in knownDataSet if datapoint[-1] == label]
            assert(dataOfSpecificLabel == self.testClassifier.dataSplitByClass[label])
        self.splitDataByClass = self.testClassifier.dataSplitByClass

    def testDistributions(self):
        for label in self.testClassifier.featureDistributionsByClass:
            print("Distributions for label: ", label)
            for distribution in self.testClassifier.featureDistributionsByClass[label]:
                print(distribution, end= '\n\n')
            print('Probability of selecting this label from the population: ', self.testClassifier.classProbabilities[label], end= '\n\n')
        
        for labelNum, label in enumerate(self.splitDataByClass):
            subset = self.splitDataByClass[label]
            for featureNum in range(len(subset[0]) - 1):
                featureSet = [dataPoint[featureNum] for dataPoint in subset]
                mean = sum(featureSet) / len(featureSet)
                squaredDiffFromMean = [(mean - dataPoint[featureNum]) ** 2 for dataPoint in subset]
                variance = sum(squaredDiffFromMean) / len(squaredDiffFromMean)
                assert(mean == self.testClassifier.featureDistributionsByClass[label][featureNum].mu)
                assert(variance == self.testClassifier.featureDistributionsByClass[label][featureNum].sigma2)
    
    def testPredictions(self):
        assert(0 == self.testClassifier.predict([3, 1]))
        assert(0 == self.testClassifier.predict([3]))
        assert(2 == self.testClassifier.predict([18]))
        assert(2 == self.testClassifier.predict([21]))
        assert(1 == self.testClassifier.predict([3, 2]))
    
if __name__ == "__main__":
    tester = NaiveBayesTester()

    tester.test()
