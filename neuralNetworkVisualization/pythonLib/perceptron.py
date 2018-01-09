import math
import numpy as np

class Perceptron():
    
    def __init__(self, weights, bias, activationType = "sigmoid"):
        self.weights = np.array([weight for weight in weights])
        self.bias = bias
        self.activationFunction = initActivationFunction(activationType)

    def initActivationFunction(self, activationType):
        activationType = activationType.lower()
        if activationType == "sigmoid":
            return Perceptron.sigmoidFunction
        elif activationType == "relu":
            return Perceptron.reluFunction
        elif activationType == "identity":
            return Perceptron.identity
        elif activationType == "binary":
            return Perceptron.binary
        elif activationType == "tangent":
            return Perceptron.tanH
        elif activationType = "arctan":
            return Perceptron.arctan
        
    def calculateOutput(self, inputs):
        weightedSum = sum(inputs * self.weights)
        biasedSum = weightedSum - self.bias
        return self.activationFunction(weightedSum)       


    def sigmoidFunction(inpt):
        return math.exp(inpt) / (math.exp(inpt) + 1)

    def reluFunction(inpt):
        if inpt > 0:
            return inpt
        else:
            return 0

    def identity(inpt):
        return inpt

    def binary(inpt):
        if inpt > 0:
            return 1
        else:
            return 0

    def tanH(inpt):
        return (2 / (1 + math.exp(-2 * inpt))) - 1

    def arctan(inpt):
        return math.atan(inpt)

if __name__ == "__main__":
    pass
