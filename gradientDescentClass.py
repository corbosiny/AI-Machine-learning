class gradientDescent():

    def __init__(self, trainingData, weights, alpha, featureScaling = False, dp = None):
        self.trainingData = trainingData
        self.inputs = [x[0] for x in trainingData]
        self.outputs = [y[1] for y in trainingData]
        self.weights = weights
        self.alpha = alpha
        self.featureScaling = featureScaling
        if dp == None:
            self.dp = 6
        else:
            self.dp = dp

        if len(self.inputs[0]) != len(weights):
            raise ValueError('Weights do not match all the inputs!')

        if featureScaling:
            self.inputs, self.ratios = self.scaleFeatures()

        self.cleanUp()

    def cleanUp(self):
        for i in range(len(self.weights)):
            self.weights[i] = round(self.weights[i], self.dp)
            
        for i in range(len(self.trainingData)):
            for j in range(len(self.trainingData[0][0])):
                self.trainingData[i][0][j] = round(self.trainingData[i][0][j], self.dp)
            self.trainingData[i][1] = round(self.trainingData[i][1], self.dp)

    def scaleFeatures(self, inputs = None):
        ratios = []
        if not inputs:
            inputs = self.inputs

        for i in range(1, len(inputs[0])):
            minVal = float(inputs[0][i])
            maxVal = float(inputs[0][i])
            for dataPoint in inputs:
                if dataPoint[i] < minVal:
                    minVal = float(dataPoint[i])
                elif dataPoint[i] > maxVal:
                    maxVal = float(dataPoint[i])
                    
            for dataPoint in inputs:
                dataPoint[i] = (dataPoint[i] - minVal) / (maxVal - minVal) 

            ratios.append([maxVal, minVal])
            
        return inputs, ratios

    def unscaleFeatures(self, inputs = None, ratios = None):
        if not inputs:
            inputs = self.inputs

        if not ratios:
            ratios = self.ratios

        for i in range(1, len(inputs[0])):
            for j in range(len(inputs)):
                inputs[j][i] = inputs[j][i] * (ratios[i - 1][0] - ratios[i - 1][1]) + ratios[i - 1][1]
            
        return inputs

    def calcCost(self, inputs, output, derivative = False):
        expected = 0
        for i, weight in enumerate(self.weights):
            expected += weight * inputs[i]

        if not derivative:
            return .5 * ((expected - output) ** 2)
        else:
            return (expected - output) * inputs[i]
        
    def calcAverageError(self, data = None):
        total = 0.0
        if not data:
            data = self.trainingData
            
        for dataPoint in data:
            total += self.calcCost(dataPoint[0], dataPoint[1])
        total = total / len(data)
        return total
        
    def adjustWeights(self):
        tempWeights = []
        
        for i in range(len(self.weights)):
            total = 0.0
            for dataPoint in self.trainingData:
                total += self.calcCost(dataPoint[0], dataPoint[1], True)     
                #print(total)
            total = total / len(self.trainingData)
            tempWeights.append(self.weights[i] - self.alpha * total)

        return tempWeights
    
    def fit(self, numSteps):
        for i in range(numSteps):
            self.weights = self.adjustWeights()
        self.cleanUp()
        return self.weights

    def predict(self, inputs, featureScale = None):
        if featureScale == None:
            featureScale = self.featureScaling
        if featureScale:
            for i in range(1, len(inputs)):
                inputs[i] = (inputs[i] - self.ratios[i - 1][1]) / float((self.ratios[i - 1][0] - self.ratios[i - 1][1]))
        output = 0.0
        for i, weight in enumerate(self.weights):
            output += weight * inputs[i]
        return output

    def __str__(self):
        string = 'Weights: '
        for weight in self.weights:
            string += str(weight) + ' '
        string += '\nData: '
        string += str(self.trainingData)
        string += '\nAlpha: ' + str(self.alpha)
        string += '\nFeature Scaling: ' + str(self.featureScaling)
        return string
    
if __name__ == "__main__":
    trainingData = [[[1,4], 110],[[1,5], 135],[[1,6], 160],[[1,7], 185],[[1,8], 210]]
    weights = [-5,-8]
    
    grad = gradientDescent(trainingData, weights, .001, True, 3)
    print(grad.fit(400000))
    print()
    for i in range(len(trainingData)):
        print(grad.inputs[i])
        print(grad.outputs[i])
        print(grad.predict(trainingData[i][0], False))
        print()
    print('Final Test:')
    print(9 * 25 + 10)
    print(grad.predict([1,9]))
