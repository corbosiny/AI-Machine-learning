from perceptron import Perceptron
import matplotlib.pyplot as plt
import numpy as np
import random, math

class PerceptronTester():
    
    def __init__(self, activationType= "sigmoid"):
        self.activationType = activationType
        self.perceptronToTest = None
        self.weights = np.array([1,2,-1])

    def testPerceptron(self):
        self.testInitialization()
        self.plotActivationFunction()
        self.testOutputs()
        
        self.labelPlot()
        plt.show()
        
    def testInitialization(self):
        self.perceptronToTest = Perceptron(self.weights, activationType= self.activationType)
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
        nonWeightedInputs, weightedSumOfInputs = self.weightAndSumInputs()  
        activationOutputs = self.compareActivationOutputs(weightedSumOfInputs)
        
        plt.plot(weightedSumOfInputs, activationOutputs, 'rs')

        
    def weightAndSumInputs(self, numTest = 100):
        inputSets, weightedSumOfInputs = [], []
        for testNum in range(numTest):
            inputSets.append([random.randint(-5, 5) for x in range(len(self.weights))])
            weightedSumOfInputs.append(sum(inputSets[testNum] * self.weights))
            
        return inputSets, weightedSumOfInputs


    def compareActivationOutputs(self, weightedSumOfInputs):
        myActivationResults = [self.activationFunction(result) for result in weightedSumOfInputs]
        perceptronActivationResults = [self.perceptronToTest.activationFunction(result) for result in weightedSumOfInputs]
        for dataPoint in range(len(myActivationResults)):
            assert(myActivationResults[dataPoint] == perceptronActivationResults[dataPoint])
        return perceptronActivationResults


        
    def activationFunction(self, inpt):
        if self.activationType == "sigmoid":
            return math.exp(inpt) / (math.exp(inpt) + 1)
        elif self.activationType == "identity":
            return inpt
        elif self.activationType == "binary":
            if inpt > 0:
                return 1
            else:
                return 0
        elif self.activationType == "relu":
            return max([0, inpt])
        elif self.activationType == "tangent":
            return (2 / (1 + math.exp(-2 * inpt))) - 1
        elif self.activationType == "arctan":
            return math.atan(inpt)
            

    def labelPlot(self):
        plt.legend(['Our test activation function', self.activationType + ' activation function'])
        plt.xlabel('inputs to activation function')
        plt.ylabel('output of activation function')
    
if __name__ == "__main__":
    tester = PerceptronTester('relu')
    tester.testPerceptron()
