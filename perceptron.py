import math
import numpy as np

class Perceptron():
    
    def __init__(self, weights):
        self.weights = np.array([weight for weight in weights])

    def calculateOutput(self, inputs):
        weightedSum = self.weightAndSumInputs(inputs)
        return self.activationFunction(weightedSum)

    def weightAndSumInputs(self, inputs):
        return sum(inputs * self.weights)        

    def activationFunction(self, inpt):
        return math.exp(inpt) / (math.exp(inpt) + 1)

