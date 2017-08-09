import numpy as np
import math
import random

class StochasticGradientDescent():

    def __init__(alpha, weights = None, powers = None):
        self.weights = weights
        self.powers = powers

    def fit(trainingSet, numIterations = 20000):

        self.initWeightsAndPowers(len(trainingSet) - 1) #excluding the 
        
        self.trainingSet = self.scaleFeatures(trainingSet)
        self.dataGenerator = self.initDataGenerator()
        
        for iteration in range(numIterations):
            adjustments = self.calculateAdjustmentsNeededForModel()
            self.adjustModelWeights(adjustments)

        return self.weights

    def initWeightsAndPowers(self, numWeights):
        if not self.weights:
            self.weights = [random.randint(-10, 10) for x in range(numWeights)]

        if not self.powers:
            self.powers = []


    def scaleFeatures(featureSet):
        total = sum(featureSet)
        sacledFeatureSet = [float(feature / total) for feature in featureSet]
        return scaledFeatureSet

    def initDataGenerator(self):
        for point in self.trainingSet:
            yield point

    
    def calculateAdjustmentsNeededForModel():
        currentAdjustments = []
        dataPoint = self.getDataPoint()
        for i in range(len(self.weights)):
            currentAdjustments.append( self.calculateAdjustment(dataPoint, i) )

        return currentCost


    def getDataPoint(self):
            try:
                return next(self.dataGenerator)
            except:                                                     #triggers when we've gone all the way through our data
                self.dataGenerator = self.initDataGenerator()
                return next(self.dataGenerator)

    
    def calculateAdjustment(self, dataPoint, indexNum):
        actualOutput = dataPoint.pop()
        inputs = [feature for feature in dataPoint]
        
        predictedOutput = self.calculateFeatureOutput(inputs)
        cost = (actualOutput - predictedOutput) * self.weights[indexNum]
        return cost


    def adjustModelWeights(self, adjustments):
        for index, weight in enumerate(self.weights):
            adjustemt = self.learningRate * adjustments
            self.weights[i] += adjustment


    def calculateFeatureOutput(self, feature, weight, power):
        return weight * math.pow(feature, power)


    def predictModelOutput(self, inputs):
        output = 0
        for i, feature in enumerate(inputs):
            output += self.calculateFeatureOutput(feature, self.weights[i], self.powers[i])
        return output
        

        
    

if __name__ == "__main__":
    
