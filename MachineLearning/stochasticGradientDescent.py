import numpy as np
import math
import random
from featureScaler import FeatureScaler


class StochasticGradientDescent():

    eps = .00000001

    def __init__(self, trainingSet, weights = None, learningRate = .001, momentumRate = .9, RMSrate = .9, activationType= 'linear'):
        self.weights = weights
        self.learningRate = learningRate
        self.momentumRate = momentumRate
        self.RMSrate = RMSrate
        self.activationType = activationType
        
        if weights is None:
            self.weights = self.initWeights(len(trainingSet[0])) 
        else:
            self.weights = weights

        self.momentums = [0 for weight in self.weights]
        self.RMSgradients = [0 for weight in self.weights]
        
        self.trainingSet = self.scaleFeatures(trainingSet)
        self.dataGenerator = self.initDataGenerator()
                
    def fit(self, numIterations = 200000):
        for iteration in range(numIterations):
            adjustments = self.calculateAdjustmentsNeededForModel(iteration)
            self.adjustModelWeights(adjustments)

        return self.weights

    def initWeights(self, numWeights):
        return [random.randint(-10, 10) for x in range(numWeights)]


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
        random.shuffle(self.trainingSet)
        for point in self.trainingSet:
            yield point

    
    def calculateAdjustmentsNeededForModel(self, iteration):
        self.currentBatch = self.getBatch()
        currentAdjustments = []
        for i in range(len(self.weights)):
            gradient  = self.calculateLookAheadGradient(i)
            self.RMSgradients[i] = self.RMSgradients[i] * self.RMSrate + (1 - self.RMSrate) * math.pow(gradient, 2)
            self.RMSgradients[i] *= 1 / (1 - math.pow(self.RMSrate, iteration + 1))
            self.momentums[i] = (self.momentums[i] * self.momentumRate) +  ((1 - self.momentumRate) * gradient)
            self.momentums[i] *= 1 / (1 - math.pow(self.momentumRate, iteration + 1))
            currentAdjustments.append(self.momentums[i] / np.sqrt(self.RMSgradients[i]) + StochasticGradientDescent.eps)

        return currentAdjustments


    def getBatch(self, numDataPoints = 3):
        return [self.getDataPoint() for i in range(numDataPoints)]
            

    def getDataPoint(self):
            try:
                return next(self.dataGenerator)
            except:                                                     #triggers when we've gone all the way through our data
                self.dataGenerator = self.initDataGenerator()
                return next(self.dataGenerator)


    def calculateLookAheadGradient(self, weightNum):
            
            self.weights = [weight -  (self.momentums[weightNum] * self.momentumRate) for weight in self.weights]
            gradient = self.calculateErrorOfCurrentBatch(weightNum)
            self.weights = [weight + (self.momentums[weightNum] * self.momentumRate) for weight in self.weights]
            return gradient
        
    def calculateErrorOfCurrentBatch(self, weightNum):
        totalCost = 0
        for dataPoint in self.currentBatch:
            actualOutput = dataPoint[-1]
            predictedOutput = self.calculateOutput(dataPoint[:-1])
            if self.activationType == 'linear':
                if weightNum == 0:
                    totalCost += (predictedOutput - actualOutput)
                else:
                    totalCost += (predictedOutput - actualOutput) * dataPoint[weightNum - 1]
            elif self.activationType == 'logistic':
                if weightNum == 0:
                    totalCost += (predictedOutput - actualOutput) * predictedOutput * (1 - predictedOutput)
                else:
                    totalCost += (predictedOutput - actualOutput) * dataPoint[weightNum - 1] * predictedOutput * (1 - predictedOutput)
                 
        return totalCost / float(len(self.currentBatch))


    def calculateOutput(self, dataPoint):
        if self.activationType == "linear":
            output = sum([weight * feature for weight, feature in list(zip(self.weights[1:], dataPoint))])
            output += self.weights[0]
            return output
        elif self.activationType == "logistic":
            inpt = self.weights[0] + sum([weight * feature for weight, feature in list(zip(self.weights[1:], dataPoint))])
            return StochasticGradientDescent.sigmoid(inpt)

        
    def adjustModelWeights(self, adjustments):
        for index, weight in enumerate(self.weights):
            self.weights[index] -= self.learningRate * adjustments[index]



    def predictModelOutput(self, inputs):
        scaledInputs = [scaler.featureScaleMeanPoint(inputFeature) for scaler, inputFeature in list(zip(self.featureScalers, inputs))]
        return self.calculateOutput(scaledInputs)


    def sigmoid(inpt):
        output = 0
        try:
            output =  1.0 / float(math.exp(-inpt) + 1)
        except:
            output = 0
        return output
        
    def maeError(actual, predicted):
        totalError = 0
        for i in range(len(actual)):
            totalError += abs(predicted[i] - actual[i])
        return totalError / float(len(actual))

    def rmsError(actual, predicted):
        totalError = 0
        for i in range(len(actual)):
            totalError += (predicted[i] - actual[i]) ** 2
        return totalError / float(len(actual))
    


    
if __name__ == "__main__":
    testTrainingSet = [[0, 1], [1, 0], [.5, .5]]

    #print(StochasticGradientDescent())
    testClass = StochasticGradientDescent(testTrainingSet, activationType = 'logistic')
    testClass.fit()    
    print(testClass.predictModelOutput(testTrainingSet[0][:-1]))
    print(testClass.predictModelOutput(testTrainingSet[1][:-1]))
    print(testClass.predictModelOutput(testTrainingSet[2][:-1]))
