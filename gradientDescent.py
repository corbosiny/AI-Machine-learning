import numpy

def calcCost(predictedValues, values):
    m = len(values)
    s = sum((x - y) ** 2 for x,y in list(zip(predictedValues, values)))
    
    return s / (2*m)

def adjustWeights(predictedValues, yinputs, alpha, weights, xinputs):
    tempWeights = []
    maxes = []

    for num, weight in enumerate(weights):
        #print('y: ', end='')
        #print(yinputs)
        #print('x: ', end='')
        #print(xinputs)
        diffs = [x - y for x,y in zip(predictedValues, yinputs)]
        #print('D: ', end='')
        #print(diffs)
        #print(weight)
        for num2, x in enumerate(xinputs):
            diffs[num2] *= x[num]

        #print('ND: ', end='')
        #print(diffs)
        #print('s:', end ='')
        s = sum(diffs) / len(yinputs)
        #print(s)
        tempWeights.append(weight - alpha * s)
        #print('tw: ', end='')
        #print(tempWeights)
    return tempWeights

def gradientDescent(trainingData, weights, alpha, numSteps):
    
    costs = []
    xinputs = [x[0] for x in trainingData]
    yinputs = [y[1] for y in trainingData]
    for x in range(numSteps):
        predictedValues = [numpy.dot(x, weights) for x in xinputs]
        #print('P: ', end='')
        #print(predictedValues)
        cost = calcCost(predictedValues, yinputs)
        costs.append(cost)
        
        weights = adjustWeights(predictedValues, yinputs, alpha, weights, xinputs)
        
    return (costs, weights)

def rSquared(data, predictions):
    ybar = np.mean(data)
    num = np.mean([x ** 2 for x in data - predictions])
    denom = np.mean([(y - ybar) ** 2 for y in data])
    rSquared = 1 - num / denom
    return rSquared


if __name__ == '__main__':

    trainingData = [[[1,4], 110],[[1,5], 135],[[1,6], 160],[[1,7], 185],[[1,8], 210]]
    weights = [-5,-8]
    
    cost, weights = gradientDescent(trainingData, weights, .001, 200000)
    print(weights)
