import math
import random
import matplotlib.pyplot as plt
from matrix import Matrix    #uses this for the incoming filtering ability
from PIL import Image #used for upcoming image filtering

class Gaussian():

    def __init__(self, sigmaSquared, mu = 0, tolerance = .01):
        self.mu = mu
        self.sigma2 = sigmaSquared
        if not isinstance(mu, int):
            raise ValueError('Mu must be a numerical value')
    
        if not isinstance(self.sigma2, int):                    #just checking if proper data types were entered
            raise ValueError('The variance must be numerical value')
        
        self.stdEv = math.sqrt(self.sigma2)
        self.tolerance = tolerance
        self.stepSize = .001 #adaptive step size will be implemented later on
        
    def evaluate(self, point): #returns prob of getting that exact number
        return 1 / math.sqrt(2 * math.pi * self.sigma2) * math.exp(-.5 * math.pow(point - self.mu, 2) / self.sigma2)

    def generateNoise(self, size):  #generates Guassian noise, so 68% of the noise will be within one standard deviation of the mean
        noise = []
        for i in range(size):       #fly wheel method of random choice
            beta = random.random() * self.evaluate(self.mu) * 2 #I start off with a very high(unreachable by any one number) probability
            multiplier = random.randint(-1, 1)
            while multiplier == 0: #used so I sometimes pick stuff below the mean
                multiplier = random.randint(-1, 1)
                
            choice = random.random() * multiplier * (self.mu + self.stdEv * 4) #picking my choice, anything outside of four standard deviations is just basically impossible to hit
            while self.evaluate(choice) < beta + self.tolerance:                #if the choices prob is higher than beta, pick it
                beta -= self.evaluate(choice)                                   #otherwise subtract its prob from beta and pick a new choice, this makes it so we pick higher probs much more often
                choice = random.random() * float(multiplier) * (self.mu + self.stdEv * 4)#cont. from above: and we preserve the guassian attribute of the noise based off how probability is calcualted
            
            noise.append(choice)
        return noise

    def calculateWeights(kernel, guass):                #still in progress, calculates weights for a weighted average when filtering
        scores = Matrix.zero(kernel.rows, kernel.columns)
        center = [int(kernel.rows / 2), int(kernel.columns / 2)]
        for row in range(kernel.rows):
            for column in range(kernel.columns):
                distance = math.sqrt(math.pow(row - center[0], 2) + math.pow(column - center[1], 2))
                score = guass.evaluate(distance)
                scores[row][column] = score
        return scores
    
    def applyKernel(kernel, guass):                     #still in progress, applying a filter kernel to a matrix of pixels
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

    def filter(pixels, kernelSize, guass):  #still in progress, goes over a set of pixels and applys a guassian filter to each pixel
        pass
        
    def plotGaussian(self, numPoints = 100): #used to plot and visualize the gaussian
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
    guass = Gaussian(1) #test code below to make sure everything is working
    print(guass.evaluate(1))
    print(guass.evaluate(-10))
    print(guass.generateNoise(15))
    #guass.plotGaussian()
    kernel = Matrix([[3,2,3], [2,4,2],[5,1,4]])
    print(Gaussian.applyKernel(kernel, guass))
    print(guass.returnProbDensity(-1))
    print(guass.returnProbDensity(1))
    print(guass.returnProbDensity(1) - guass.returnProbDensity(-1))
    
