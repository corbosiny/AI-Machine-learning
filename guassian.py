from __future__ import division
import math
import random
import matplotlib.pyplot as plt
from matrix import Matrix    #uses this for the incoming filtering ability
from PIL import Image #used for upcoming image filtering

class Gaussian():

    def __init__(self, sigmaSquared, mu = 0, tolerance = .001):
        if not isinstance(mu, int) and not isinstance(mu, float):
            raise ValueError('Mu must be a numerical value')
    
        if not isinstance(sigmaSquared, int) and not isinstance(sigmaSquared, float):                    #just checking if proper data types were entered
            raise ValueError('The variance must be numerical value')

        self.mu = float(mu)
        self.sigma2 = float(sigmaSquared)
        
        self.stdEv = math.sqrt(self.sigma2)
        self.tolerance = tolerance
        self.stepSize = tolerance #this is an arbitrary value we give it before adjusting the step size, the function to adjust needs a prior stepsize
        self.stepSize = self.adaptStepSize(mu) #adapts step size for the given tolerance

    def evaluate(self, point): #returns prob of getting that exact number
        return 1 / math.sqrt(2 * math.pi * self.sigma2) * math.exp(-.5 * math.pow(point - self.mu, 2) / self.sigma2)

    def generateNoise(self, size):  #generates Guassian noise, so 68% of the noise will be within one standard deviation of the mean
        noise = []
        self.stepSize = .001
        for i in range(size):       #fly wheel method of random choice
            beta = random.random() * self.evaluate(self.mu) * 2 #I start off with a very high(unreachable by any one number) probability
            multiplier = random.randint(-1, 1)
            while multiplier == 0: #used so I sometimes pick stuff below the mean
                multiplier = random.randint(-1, 1)
                
            choice = random.random() * multiplier * (self.mu + self.stdEv * 4) #picking my choice, anything outside of four standard deviations is just basically impossible to hit
            while self.evaluate(choice) < beta + self.tolerance:                #if the choices prob is higher than beta, pick it
                beta -= self.evaluate(choice)                                   #otherwise subtract its prob from beta and pick a new choice, this makes it so we pick higher probs much more often
                choice = random.random() * multiplier * (self.mu + self.stdEv * 4)#cont. from above: and we preserve the guassian attribute of the noise based off how probability is calcualted
            
            noise.append(choice)
        self.stepSize = self.adaptStepSize(self.mu)
        return noise

    def calculateWeights(kernel, guass):                #still in progress, calculates weights for a weighted average when filtering
        scores = Matrix.zero(kernel.rows, kernel.columns)
        center = [int(kernel.rows / 2), int(kernel.columns / 2)]
        total = 0
        for row in range(kernel.rows):
            for column in range(kernel.columns):
                distance = math.sqrt(math.pow(row - center[0], 2) + math.pow(column - center[1], 2))
                score = guass.evaluate(distance)
                scores[row][column] = score
                total += score
        for row in range(kernel.rows):
            for column in range(kernel.columns):
                scores[row][column] /= total
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
        
        return total

    def filter(pixels, kernelSize, guass):  #still in progress, goes over a set of pixels and applys a guassian filter to each pixel
        for num, x in enumerate(pixels):
            kernel = Matrix.zero(kernelSize, kernelSize)
            for y in range(kernelSize):
                
        
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
        x = self.mu - self.stdEv * 4.0 
        while x < num:
            prob += self.evaluate(x) * self.stepSize
            x += self.stepSize
            self.stepSize = self.adaptStepSize(x)
        return prob

    def adaptStepSize(self, num):   #calculates the local truncation error then calculates the new given step size for a certain tolerance
        vel = self.evaluate(num)
        eulerPos = vel * self.stepSize
        eulerVel = self.evaluate(num + self.stepSize)
        heunsVel = (eulerVel + vel) / 2
        heunsPos = heunsVel * self.stepSize
        time = 2 * (self.mu + self.stdEv * 3) / self.stepSize 
        error = abs(heunsPos - eulerPos) +  time * abs(heunsVel - eulerVel)
        newStepSize =  self.stepSize * math.sqrt(self.tolerance / (error + math.exp(-25)))
        if self.stdEv > 1: #this just makes sure our step sizes dont go down too small and bring down computational time when they dont need to go that small
            return max(.001, newStepSize)
        else:
            return max(.00001, newStepSize)
    
if __name__ == "__main__":
    guass = Gaussian(1) #test code below to make sure everything is working
##    print(guass.evaluate(.15))
##    print(guass.evaluate(-.15))
##    print(guass.tolerance)
##    print(guass.generateNoise(15))
##    #guass.plotGaussian()
    kernel = Matrix([[1,1,1,2,1,1,1], [1,1,2,2,2,1,1],[1,1,1,2,1,1,1]])
    print(Gaussian.applyKernel(kernel, guass))
##    print(guass.returnProbDensity(.474) - guass.returnProbDensity(-.474))
    im = Image.open('img.png')

    pixels = list(im.getdata())
    pixelsFlat = []
    for x in pixels:
        for y in x:
            pixelsFlat.append(y)
    print(pixelsFlat[1:5])
    width, height = im.size
    print(width, height)
    pixelNum = 0
    while pixelsFlat[pixelNum] == 0:
        pixelNum += 1

