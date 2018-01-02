from naiveBayesClassifier import NaiveBayesClassifier
import random

knownDataSet = [[3, 1, 0],[4, 1, 0], [5, 1, 0], [13, 1],[14, 1],[15, 1], [20, 2], [20, 2], [21, 2], [3,2,4]]

class NaiveBayesTester():

    def __init__(self, dataset = knownDataSet):
        self.testDataSet = dataset
        self.testClassifier = NaiveBayesClassifier(self.testDataSet)

    def test(self, datapoint = [5,2]):
        print("Testing with dataset: ", self.testDataSet)
        print('_' * 25)
        assert(self.testDataSet == self.testClassifier.trainingSet)

        
        self.testClassifier.fit()

        for label in self.testClassifier.dataSplitByClass:
            dataOfSpecificLabel = [datapoint for datapoint in knownDataSet if datapoint[-1] == label]
            assert(dataOfSpecificLabel == self.testClassifier.dataSplitByClass[label])

        
        for label in self.testClassifier.featureDistributionsByClass:
            print("Distributions for label: ", label)
            for distribution in self.testClassifier.featureDistributionsByClass[label]:
                print(distribution, end= '\n\n')
            print('Probability of selecting this label from the population: ', self.testClassifier.classProbabilities[label], end= '\n\n')
        

        print("Prediction for label of test data point: ", self.testClassifier.predict(datapoint))
        
if __name__ == "__main__":
    tester = NaiveBayesTester()

    tester.test()
