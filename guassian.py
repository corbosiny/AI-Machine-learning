import math
import random
import matplotlib.pyplot as plt
from matrix import Matrix
from PIL import Image

class Gaussian():

    def __init__(self, sigmaSquared, mu = 0, tolerance = .01):
        self.mu = mu
        self.sigma2 = sigmaSquared
        if not isinstance(mu, int):
            raise ValueError('Mu must be a numerical value')

        if not isinstance(self.sigma2, int):
            raise ValueError('The variance must be numerical value')
        
        self.stdEv = math.sqrt(self.sigma2)
        self.tolerance = tolerance
        self.stepSize = .001 #adaptive step size will be implemented later on
        
    def evaluate(self, point): #returns prob of getting that exact number
        return 1 / math.sqrt(2 * math.pi * self.sigma2) * math.exp(-.5 * math.pow(point - self.mu, 2) / self.sigma2)

    def generateNoise(self, size):
        noise = []
        for i in range(size):
            beta = random.random() * self.evaluate(self.mu) * 2
            multiplier = random.randint(-1, 1)
            while multiplier == 0:
                multiplier = random.randint(-1, 1)
                
            choice = random.random() * multiplier * (self.mu + self.stdEv * 4)
            while self.evaluate(choice) < beta + self.tolerance:
                beta -= self.evaluate(choice)
                choice = random.random() * float(multiplier) * (self.mu + self.stdEv * 4)
            
            noise.append(choice)
        return noise

    def calculateWeights(kernel, guass):
        scores = Matrix.zero(kernel.rows, kernel.columns)
        center = [int(kernel.rows / 2), int(kernel.columns / 2)]
        for row in range(kernel.rows):
            for column in range(kernel.columns):
                distance = math.sqrt(math.pow(row - center[0], 2) + math.pow(column - center[1], 2))
                score = guass.evaluate(distance)
                scores[row][column] = score
        return scores
    
    def applyKernel(kernel, guass):
        if not isinstance(kernel, Matrix):
            raise ValueError("Kernel must be a matrix")

        if not isinstance(guass, Gaussian):
            raise ValueError("A Guassian object must be entered")

        scores = Gaussian.calculateWeights(kernel, guass)
        total = 0
        for row in range(scores.rows):
            for column in range(scores.columns):
                total += scores[row][column] * kernel[row][column]
        #total /= scores.rows * scores.columns
        kernel[int(kernel.rows/2)][int(kernel.columns/2)] = total
        
        return kernel[int(kernel.rows/2)][int(kernel.columns/2)]

    def filter(pixels, kernelSize, guass):
        pass
        
    def plotGaussian(self, numPoints = 100):
        X = []
        Y = []
        x = self.mu - 4 * self.stdEv
        while x < self.mu + 4 * self.stdEv:
            X.append(x)
            Y.append(self.evaluate(x))
            x += (self.mu + 4 * self.stdEv * 2) / numPoints

        plt.plot(X,Y)
        plt.show()


    def returnProbDensity(self, num):  #returns the prob of getting a value of equal to or less than the given value with the distribution parameters
        prob = 0
        x = self.mu - self.stdEv * 4 
        while x < num:
            prob += (self.evaluate(x) + self.evaluate(x + self.stepSize)) * self.stepSize * .5
            x += self.stepSize
        return prob
    
if __name__ == "__main__":
    guass = Gaussian(1)
    print(guass.evaluate(1))
    print(guass.evaluate(-10))
    print(guass.generateNoise(15))
    #guass.plotGaussian()
    kernel = Matrix([[3,2,3], [2,4,2],[5,1,4]])
    print(Gaussian.applyKernel(kernel, guass))
    print(guass.returnProbDensity(-1))
    print(guass.returnProbDensity(1))
    print(guass.returnProbDensity(1) - guass.returnProbDensity(-1))
    
