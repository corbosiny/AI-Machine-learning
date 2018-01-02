from stochasticGradientDescent import StochasticGradientDescent
from featureScaler import FeatureScaler

testTrainingDataSet = [[1, 3], [2, 5], [3, 7]]

class StochasticGradientDescentTester():


    def __init__(self):
        self.testClass = StochasticGradientDescent(testTrainingDataSet)
        splitFeatures = [[datapoint[num] for datapoint in testTrainingDataSet] for num in range(len(testTrainingDataSet[0]) - 1)]
        scaledSplitFeatures = [FeatureScaler(setOfSplitFeature).featureScaleMean() for setOfSplitFeature in splitFeatures]

        for featureNum, scaledFeature in enumerate(scaledSplitFeatures):
            assert(scaledFeature == self.testClass.scaledSetOfFeatureInstances[featureNum])

    def test(self):
        splitFeatures = [[datapoint[num] for datapoint in testTrainingDataSet] for num in range(len(testTrainingDataSet[0]) - 1)]
        scaledSplitFeatures = [FeatureScaler(setOfSplitFeature).featureScaleMean() for setOfSplitFeature in splitFeatures]

        for featureNum, scaledFeature in enumerate(scaledSplitFeatures):
            assert(scaledFeature == self.testClass.scaledSetOfFeatureInstances[featureNum])

        scaledDataSet = zip(*(scaledSplitFeatures))
        scaledDataSet = [list(datapoint) for datapoint in scaledDataSet]

        for num in range(len(testTrainingDataSet)):
            scaledDataSet[num].append(testTrainingDataSet[num][-1])

        for datapoint in scaledDataSet:
            compare = next(self.testClass.dataGenerator)
            assert(datapoint == compare)

        print(self.testClass.fit())
        print(self.testClass.predictModelOutput([1]))
        
if __name__ == "__main__":
    tester = StochasticGradientDescentTester()
    tester.test()
