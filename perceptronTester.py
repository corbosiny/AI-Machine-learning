from perceptron import Perceptron
import matplotlib.pyplot as plt
import numpy as np
import random, math

class PerceptronTester():
    
    def __init__(self):
        self.perceptronToTest = None
        self.weights = np.array([1,2,-1])

    def testPerceptron(self):
        self.testInitialization()
        self.plotActivationFunction()
        self.testOutputs()
        self.testGradientDescent()
        
        self.labelPlot()
        plt.show()
        
    def testInitialization(self):
        self.perceptronToTest = Perceptron(self.weights)
        self.testExistance()
        self.testMemberVariables()
        
    def testExistance(self):
        assert(self.perceptronToTest is not None)

    def testMemberVariables(self):
        for weightIndex in range(len(self.weights)):
            assert(self.weights[weightIndex] == self.perceptronToTest.weights[weightIndex])

    def plotActivationFunction(self):
        inputs = [x for x in range(-10, 10)]
        outputs = [self.activationFunction(x) for x in inputs]
        plt.plot(inputs, outputs)

    def testOutputs(self):
        nonWeightedInputs, weightedSumOfInputs = self.testWeightedSummingOfInputs()  
        activationOutputs = self.compareActivationOutputs(weightedSumOfInputs)
        self.compareFinalOutputs(nonWeightedInputs, activationOutputs)
        
        plt.plot(weightedSumOfInputs, activationOutputs, 'rs')

        
    def testWeightedSummingOfInputs(self, numTest = 100):
        inputSets, weightedSumOfInputs = [], []
        for testNum in range(numTest):
            inputSets.append([random.randint(-5, 5) for x in range(len(self.weights))])
            weightedSumOfInputs.append(sum(inputSets[testNum] * self.weights))
            assert(weightedSumOfInputs[testNum] == self.perceptronToTest.weightAndSumInputs(inputSets[testNum]))
        return inputSets, weightedSumOfInputs


    def compareActivationOutputs(self, weightedSumOfInputs):
        myActivationResults = [self.activationFunction(result) for result in weightedSumOfInputs]
        perceptronActivationResults = [self.perceptronToTest.activationFunction(result) for result in weightedSumOfInputs]
        for myResult, testResult in zip(myActivationResults, perceptronActivationResults):
            assert(myResult == testResult)
        return myActivationResults


    def compareFinalOutputs(self, inputs, resultsToTestAgainst):
        perceptronResults = [self.perceptronToTest.calculateOutput(inputSet) for inputSet in inputs]
        for perceptronResult, resultToTestAgainst in zip(perceptronResults, resultsToTestAgainst):
            assert(perceptronResult == resultToTestAgainst)
        
    def activationFunction(self, inpt):
        return math.exp(inpt) / (math.exp(inpt) + 1)


    def testGradientDescent(self):
        pass


    def labelPlot(self):
        plt.legend(['Our test activation function', 'perceptron activation function'])
        plt.xlabel('inputs to activation function')
        plt.ylabel('output of activation function')
    
if __name__ == "__main__":
    tester = PerceptronTester()
    tester.testPerceptron()
