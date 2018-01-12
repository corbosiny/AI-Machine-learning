from stochasticGradientDescent import StochasticGradientDescent
from featureScaler import FeatureScaler
import matplotlib.pyplot as plt
testTrainingDataSet = [[1, 3], [2, 5], [3, 7]]

class StochasticGradientDescentTester():


    def __init__(self):
        self.testClass = StochasticGradientDescent(testTrainingDataSet)
        splitFeatures = [[datapoint[num] for datapoint in testTrainingDataSet] for num in range(len(testTrainingDataSet[0]) - 1)]
        scaledSplitFeatures = [FeatureScaler(setOfSplitFeature).featureScaleMean() for setOfSplitFeature in splitFeatures]

        for featureNum, scaledFeature in enumerate(scaledSplitFeatures):
            assert(scaledFeature == self.testClass.scaledSetOfFeatureInstances[featureNum])

    def test(self):
        scaledDataSet = self.testFeatureScaling()
        self.testDataGenerator(scaledDataSet)
        self.testFitting()
        self.plotGradientDescent()
        print("Test passed!")

    def testFeatureScaling(self):
        splitFeatures = [[datapoint[num] for datapoint in testTrainingDataSet] for num in range(len(testTrainingDataSet[0]) - 1)]
        scaledSplitFeatures = [FeatureScaler(setOfSplitFeature).featureScaleMean() for setOfSplitFeature in splitFeatures]

        for featureNum, scaledFeature in enumerate(scaledSplitFeatures):
            assert(scaledFeature == self.testClass.scaledSetOfFeatureInstances[featureNum])

        scaledDataSet = zip(*(scaledSplitFeatures))
        scaledDataSet = [list(datapoint) for datapoint in scaledDataSet]
        
        for num in range(len(testTrainingDataSet)):
            scaledDataSet[num].append(testTrainingDataSet[num][-1])

        return scaledDataSet
    
    def testDataGenerator(self, scaledDataSet):
        classifierDataSet = [next(self.testClass.dataGenerator) for datapoint in scaledDataSet]
        for datapoint in scaledDataSet:
            assert(datapoint in classifierDataSet)

    def testFitting(self):
        print(self.testClass.fit())
        print(self.testClass.predictModelOutput([1]))
        print(self.testClass.predictModelOutput([2]))
        print(self.testClass.predictModelOutput([3]))
        assert(abs(3 - self.testClass.predictModelOutput([1])) < .5)
        assert(abs(5 - self.testClass.predictModelOutput([2])) < .5)
        assert(abs(7 - self.testClass.predictModelOutput([3])) < .5)

    def plotGradientDescent(self):
        epochs = [epochNum for epochNum in self.testClass.totalErrorForEpochs]
        errorValues = [self.testClass.totalErrorForEpochs[epoch][0] for epoch in epochs]
        momentumValues = [self.testClass.totalErrorForEpochs[epoch][1] for epoch in epochs]
        plt.plot(epochs, errorValues)
        plt.plot(epochs, momentumValues)
        plt.legend(['Gradient over all weights for each epoch', 'Running momentum for each epoch'])
        plt.xlabel('Epoch Number')
        plt.ylabel('Gradient')
        plt.show()
    
if __name__ == "__main__":
    tester = StochasticGradientDescentTester()
    tester.test()
