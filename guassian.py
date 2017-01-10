import math
import random
import matplotlib.pyplot as plt
from matrix import Matrix
from PIL import Image

class Gaussian():

    def __init__(self, sigmaSquared, mu = 0):
        self.mu = mu
        self.sigma2 = sigmaSquared
        if not isinstance(mu, int):
            raise ValueError('Mu must be a numerical value')

        if not isinstance(self.sigma2, int):
            raise ValueError('The variance must be numerical value')
        
        self.stdEv = math.sqrt(self.sigma2)
        self.tolerance = .01
        
    def evaluate(self, point):
        return 1 / math.sqrt(2 * math.pi * self.sigma2) * math.exp(-.5 * math.pow(point - self.mu, 2) / self.sigma2)

    def generateNoise(self, size):
        noise = []
        for i in range(size):
            beta = random.random() * self.evaluate(self.mu) * 2
            choice = random.randrange(int(self.mu - self.stdEv * 4), int(self.mu + self.stdEv * 4)) + random.random()
            while self.evaluate(choice) < beta + self.tolerance:
                beta -= self.evaluate(choice)
                choice = random.randint(int(self.mu - self.stdEv * 4), int(self.mu + self.stdEv * 4))
            
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


    def returnProb(self, num):
        prob = 0
        x = self.mu - self.sigma2 * 4
        while x < num:
            prob += self.evaluate(x) * .001
            x += .001
        return prob
    
if __name__ == "__main__":
    guass = Gaussian(1)
    print(guass.evaluate(10))
    print(guass.generateNoise(15))
    #guass.plotGaussian()
    kernel = Matrix([[3,2,3], [2,4,2],[5,1,4]])
    print(Gaussian.applyKernel(kernel, guass))
    #print(guass.returnProb(-1))
    #print(guass.returnProb(1))
    #5print(guass.returnProb(1) - guass.returnProb(-1))
    
