import matrix
import math


###If using the normal equation method this code needs my matrix library, if not you can comment out the matrix import###
class GradientDescent():

    #alpha is our learning rate, feature scaling is optional and defaults to off, dp is the decimal places to round to
    def __init__(self, trainingData, weights, alpha, featureScaling = False, dp = 3):        
        self.trainingData = trainingData
        self.inputs = [x[0] for x in trainingData]      #seperating out our inputs from each datapoint
        self.outputs = [y[1] for y in trainingData]     #now seperating out the outputs from each datapoint
        self.weights = weights
        self.alpha = alpha
        self.featureScaling = featureScaling
        self.dp = dp

        if len(self.inputs[0]) != len(weights):
            raise ValueError('Weights do not match all the inputs!')

        if featureScaling:
            self.inputs, self.ratios = self.scaleFeatures()

        self.cleanUp() #rounds through all data to the presicion specified

    def cleanUp(self):
        for i in range(len(self.weights)):  
            if isinstance(self.weights[i], list):   #just going through all weights and replacing them with rounded versions
                for j in range(len(self.weights[i])):
                    self.weights[i][j] = round(self.weights[i][j], self.dp)
            else:
                self.weights[i] = round(self.weights[i], self.dp)
            
        for i in range(len(self.trainingData)):     #going through all data points and rounding them to the sepcified number of decimal places
            for j in range(len(self.trainingData[0][0])):
                self.trainingData[i][0][j] = round(self.trainingData[i][0][j], self.dp)
            self.trainingData[i][1] = round(self.trainingData[i][1], self.dp)
            

    def scaleFeatures(self, inputs = None):     #scales all features onto a rnage of 0 to 1 where 1 is the largest feature and 0 is smallest, greatly speeds up the process
        ratios = []
        if not inputs:
            inputs = self.inputs    #made inputs paramters so you could use this with other data

        for i in range(0, len(inputs[0])):  #going through each feature and finding our ranges
            minVal = float(inputs[0][i])
            maxVal = float(inputs[0][i])
            for dataPoint in inputs:
                if dataPoint[i] < minVal:
                    minVal = float(dataPoint[i])
                elif dataPoint[i] > maxVal:
                    maxVal = float(dataPoint[i])
                    
            for dataPoint in inputs:    #scaling each data point's features based on the ranges
                try:
                    dataPoint[i] = (dataPoint[i] - minVal) / (maxVal - minVal) 
                except ZeroDivisionError:
                    dataPoint[i] = minVal 
                    
            ratios.append([maxVal, minVal])
            
        return inputs, ratios   #returns the feature scaled inputs and the scale ranges for any future scaling

    def unscaleFeatures(self, inputs = None, ratios = None):        #undoes exactly what we do in the function above
        if not inputs:
            inputs = self.inputs

        if not ratios:
            ratios = self.ratios

        for i in range(1, len(inputs[0])):
            for j in range(len(inputs)):
                inputs[j][i] = inputs[j][i] * (ratios[i - 1][0] - ratios[i - 1][1]) + ratios[i - 1][1]
            
        return inputs

    def calcCost(self, inputs, output, derivative = False, num = None): #compares the estimated value to the actual value
        expected = 0
        for i, weight in enumerate(self.weights): #finding our expected value by multiplying wieghts with their repsective features
            expected += weight * inputs[i]
        
        if not derivative:                          
            return .5 * ((expected - output) ** 2)   #our cost function, notice the square helps it become differentiable
        else:
            return (expected - output) * inputs[num] #if we are finding the gradient of the cost we use this one, its the derivative of the cost function
        
    def calcAverageError(self, data = None):    #calculates the average error of each data point from its estimated value, used to see accuracy of the model
        total = 0.0
        if not data:
            data = self.trainingData
            
        for dataPoint in data:
            total += self.calcCost(dataPoint[0], dataPoint[1])
        total = total / len(data)
        return total
        
    def adjustWeights(self):
        tempWeights = []
        
        for i in range(len(self.weights)):      #going through each weight
            total = 0.0
            for dataPoint in self.trainingData:     #summing the total cost
                total += self.calcCost(dataPoint[0], dataPoint[1], self.featureScaling, i)     
                
            total = total / len(self.trainingData) #averaging the total cost
            tempWeights.append(self.weights[i] - self.alpha * total) #adjusting the weight based off this gradient

        return tempWeights
    
    def fit(self, numSteps= 5000, normal = False):        #runs through adjusting the weights and rounding them to the specified presicion for the number of steps entered
        if not normal:
            for i in range(numSteps):
                self.weights = self.adjustWeights()
            self.cleanUp()
            return self.weights
        else:
            pass

    def predict(self, inputs, featureScale = None): #takes in a data point and predicts the output useing the current estimated weights
        if featureScale == None:
            featureScale = self.featureScaling
            
        if featureScale:                #if feature scaling is turned on we gotta feature scale the incoming points
            for i in range(len(inputs)):
                try:
                    inputs[i] = (inputs[i] - self.ratios[i][1]) / float((self.ratios[i][0] - self.ratios[i][1]))
                except:
                    inputs[i] = self.ratios[i][0]
                    
        output = 0.0
        for i, weight in enumerate(self.weights): #summing and multiplying every weight with their repsective feature on the data point
            output += weight * inputs[i]
        return output

    def normalEquation(self):               #uses matricies to skip the iterative process, more about this method can be looked up
        inputMatrix = matrix.Matrix(self.inputs)
        outputMatrix = matrix.Matrix([[y] for y in self.outputs])
        inverse = (inputMatrix.transpose() * inputMatrix).inverse()
        weights = inverse * inputMatrix.transpose() * outputMatrix
        return weights
    
    def __str__(self):
        string = 'Weights: '
        for weight in self.weights:
            string += str(weight) + ' '
        string += '\nData: '
        string += str(self.trainingData)
        string += '\nAlpha: ' + str(self.alpha)
        string += '\nFeature Scaling: ' + str(self.featureScaling)
        return string

