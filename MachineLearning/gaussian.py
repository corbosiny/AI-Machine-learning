from __future__ import division
import math
import random
import matplotlib.pyplot as plt


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
        try:
            return math.exp(- ((self.mu - point) ** 2) / (self.sigma2) / 2.0) / math.sqrt(2 * math.pi * self.sigma2)           
        except:
            return point == self.mu

    def generateGaussianNoise(self):
        initialProbabilityScore = random.random() * self.evaluate(self.mu) * 2
        probabilityOfScore = 0
        while initialProbabilityScore > probabilityOfScore:
            choice = random.randrange(int(self.mu - self.stdEv * 5.0), int(self.mu + self.stdEv * 5.0))
            probabilityOfChoice = self.evaluate(choice)
            initialProbabilityScore -= probabilityOfChoice
            
        return choice 

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

    def __add__(self, b):       #merging two gaussians or adding a constant
        if isinstance(b, Gaussian):
            newMean = self.mu + b.mu    #if b is a gaussian we add the means and the variances together
            newSigma = self.sigma2 + b.sigma2
            result = Gaussian(newSigma, newMean)
            return result
        elif isinstance(b, int) or isinstance(b, float):
            result = Gaussian(self.sigma2, self.mu + b) #if b is a constant we just shift the mean over by the constant
            return result
        else:
            raise ValueError("Unsuppported operation between Gaussian and type %s" % type(b))

    def __sub__(self, b):
        return self + (-1 * b)  #just add the negative of b, used so I dont have to repeat the above add function

    def __mul__(self,b):            
        if isinstance(b, int) or isinstance(b, float):  #if int or float, then just shift the mean by multiplying it
            newMean = self.mu * b
            newSigma2 = math.pow(self.stdEv * b, 2) #the new stdEv is also multiplied so the new var is squared by that
            result = Gaussian(newSigma2, newMean)
            return result
        elif isinstance(b, Gaussian):
            newMean = (self.mu * b.sigma2 + self.sigma2 * b.mu) / (self.sigma2 + b.sigma2) #new mean is weighted average based off of variances
            newSigma2 = (self.sigma2 * b.sigma2) / (b.sigma2 + self.sigma2) #new variance is smaller than either before it
            result = Gaussian(newSigma2, newMean)
            return result
        else:
            raise ValueError("Unsuppported operation between Gaussian and type %s" % type(b))

    def __floordiv__(self, b):          #just do the mul function with one over b to save me from retyping stuff
        if not isinstance(b, int) and not isinstance(b, float):
            raise ValueError("Unsuppported operation between Gaussian and type %s" % type(b))
        else:
            return self * (1.0 / b)
        
    def __truediv__(self, b):   #just do the mul function with one over b to save me from retyping stuff
        if not isinstance(b, int) and not isinstance(b, float):
            raise ValueError("Unsuppported operation between Gaussian and type %s" % type(b))
        else:
            return self * (1.0 / b)

    def __str__(self): #returns all the info about the Gaussian
        string = ""
        string += "Mean: %.3f\n" % self.mu
        string += "Variance: %.3f\n" % self.sigma2
        string += "StdDev: %.3f" % self.stdEv
        return string
    
if __name__ == "__main__":
    gauss = Gaussian(8, 10) #test code below to make sure everything is working
    gauss2 = Gaussian(2, 13)
    print("Added: \n" + str(gauss + gauss2))
    print("Multiplied: \n" + str(gauss * gauss2))
    noise = [gauss.generateGaussianNoise() for i in range(1000)]
    noiseMean = sum(noise)  / len(noise)
    noiseVar = sum([math.pow(x - noiseMean, 2) for x in noise]) / len(noise)
    print("Mean of noise:", noiseMean)
    print("Variamce of noise:", noiseVar)
    numBins = 15
    plt.hist(noise, numBins)
    plt.show()
