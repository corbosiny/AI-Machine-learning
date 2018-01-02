import numpy as np
import math
import random
from featureScaler import FeatureScaler

#THIS IS STILL UNDER CONSTRUCTION AND IS NOT WORKING YET!!!!!

class StochasticGradientDescent():

    def __init__(self, trainingSet, weights = None, learningRate = .0001):
        self.weights = weights
        self.learningRate = learningRate
        self.featureScaler = FeatureScaler(trainingSet)
        
        if weights is None:
            self.initWeights(len(trainingSet[0])) 
        else:
            self.weights = weights
            
        self.trainingSet = self.scaleFeatures(trainingSet)
        self.dataGenerator = self.initDataGenerator()
                
    def fit(self, numIterations = 2000000):
        for iteration in range(numIterations):
            adjustments = self.calculateAdjustmentsNeededForModel()
            self.adjustModelWeights(adjustments)

        return self.weights

    def initWeights(self, numWeights):
        self.weights = [random.randint(-10, 10) for x in range(numWeights)]


    def scaleFeatures(self, featureSet):
        setOfFeatureInstances = [[dataPoint[featureNum] for dataPoint in featureSet] for featureNum in range(len(featureSet[0]) - 1)]
        self.featureScalers = [FeatureScaler(featureInstance) for featureInstance in setOfFeatureInstances]
        self.scaledSetOfFeatureInstances = [scaler.featureScaleMean() for scaler in self.featureScalers]
        
        scaledDataSet = zip(*(self.scaledSetOfFeatureInstances))
        scaledDataSet = [list(datapoint) for datapoint in scaledDataSet]
        
        for datapointNum, datapoint in enumerate(featureSet):
            scaledDataSet[datapointNum].append(datapoint[-1])
            
        return scaledDataSet

    def initDataGenerator(self):
        for point in self.trainingSet:
            yield point

    
    def calculateAdjustmentsNeededForModel(self):
        currentAdjustments = []
        dataPoint = self.getDataPoint()
        actualOutput = dataPoint[-1]
        inputs = [feature for feature in dataPoint[:-1]]

        predictedOutput = self.weights[0] + sum([weight * feature for weight, feature in list(zip(self.weights[1:], inputs))])
        for i in range(len(self.weights)):
            currentAdjustments.append(self.calculateAdjustment(actualOutput, i, predictedOutput))

        return currentAdjustments


    def getDataPoint(self):
            try:
                return next(self.dataGenerator)
            except:                                                     #triggers when we've gone all the way through our data
                self.dataGenerator = self.initDataGenerator()
                return next(self.dataGenerator)

    
    def calculateAdjustment(self, actualOutput, indexNum, predictedOutput):
        gradient = (predictedOutput - actualOutput) * self.weights[indexNum]
        return gradient


    def adjustModelWeights(self, adjustments):
        for index, weight in enumerate(self.weights):
            adjustment = self.learningRate * adjustments[index]
            self.weights[index] -= adjustment



    def predictModelOutput(self, inputs):
        scaledInputs = [scaler.featureScaleMeanPoint(inputFeature) for scaler, inputFeature in list(zip(self.featureScalers, inputs))]
        print(scaledInputs)
        output = self.weights[0]
        for i, feature in enumerate(scaledInputs):
            output += feature * self.weights[i + 1]
        return output
        

        
    

if __name__ == "__main__":
    pass
