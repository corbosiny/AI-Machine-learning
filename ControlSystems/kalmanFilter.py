from matrix import Matrix
import math
import matplotlib.pyplot as plt
import random

#requires Matrix library, in the linear algebra repository on my github!
class KalmanFilter():

    def __init__(self,stateMatrix, stateErrors, transitionMatrix, measureMatrix, measureErrors, externalTransition = None, externalMotion = None): #all we do is assign the respective matrices to our object variables, nothing special
        self.stateMatrix = stateMatrix
        self.stateErrors = stateErrors 
        self.transitionMatrix = transitionMatrix

        self.measureMatrix = measureMatrix
        self.measureErrors = measureErrors

        self.externalTransition = externalTransition #our control command transition matrix, similar to how the state transition matrix works
        self.externalMotion = externalMotion #our control commands
    
    def calcKalmanGain(self):
        totalError = self.measureMatrix * self.stateErrors * self.measureMatrix.transpose() + self.measureErrors
        return self.stateErrors * self.measureMatrix.transpose() * totalError.inverse() 

    def updateError(self, gain):              #updates erorr after a measurement, we get more accuarate after each measurement
        self.stateErrors = (Matrix.identity(2) - gain * self.measureMatrix) * self.stateErrors
        
    def updateEstimate(self, measurement):          #uses a measurment to refine its estimate
        z = Matrix([measurement])
        y = z - self.measureMatrix * self.stateMatrix
        gain = self.calcKalmanGain()

        self.stateMatrix = self.stateMatrix + (gain * y)
        self.updateError(gain)

    def updateCovariance(self):         #accumulates the error that comes from motion/adding gaussians together
        self.stateErrors = self.transitionMatrix * self.stateErrors * self.transitionMatrix.transpose()

                    
    def updateState(self, timeStep): #uses motion model to estimate the new state after a given timestep
        self.stateMatrix = self.transitionMatrix * self.stateMatrix
        if(self.externalMotion != None):
            self.stateMatrix += self.externalTransition * self.externalMotion
        self.updateCovariance()
        

###test code below here, feel free to comment out or replace when using the code###
if __name__ == "__main__":
    ##linear motion model with outside acceleration
    #NOTE: the external motion matrices are not necessary
    timeStep = 1
    stateMatrix = Matrix([[1],[0]]) #initial esimates: position of one, velocitiy of zero
    stateErrors = Matrix([[100, 0], [0, 100]]) #initial uncertanties and co-uncertanties of our estimates
    transitionMatrix = Matrix([[1, timeStep],[0, 1]]) #first row is old position + velocity times timestep
    measureMatrix = Matrix([[1, 0]])   #only measures position
    measureErrors = Matrix([[100]])    #uncertanties of sensor
    externalTransition = Matrix([[.5 * math.pow(timeStep, 2)], [timeStep]]) #first line is how the acceleration effects the position, second is how the acceleration effects velocity
    externalMotion = Matrix([[1]])  #an acceleration of 1
    
    fil = KalmanFilter(stateMatrix, stateErrors, transitionMatrix, measureMatrix, measureErrors, externalTransition, externalMotion) #starting the kalman filter
    print(stateMatrix) #printing our initial states
    print(stateErrors)
    print('-' * 20)
    print('\n')
    
    sensorNoiseMag = 5  #adding in fake noise to our sensor up to a maximmum of 5
    actualStates = [1 + .5 * math.pow(x, 2) for x in range(1, 20)] #making a fake set of "real states" to compare our filter with
    states = []
    measurements = [1 + .5 * math.pow(x, 2) + random.randint(-sensorNoiseMag, sensorNoiseMag) * random.random() for x in range(1, 20)] #simulating an array of measurments
    for measurement in measurements: #updating the filter for each measurement
        fil.updateEstimate([measurement]) #updating the state based off of a measurement
        states.append(fil.stateMatrix[0][0])    #appending the guess of the kalman filter of the state
        print('Post measurment: ')              
        print(fil.stateMatrix)                  #printing out our state estimates
        print()
        fil.updateState(timeStep)               #updating our state estimate based off of a time step
        print('Post new state Estimate: ')
        print(fil.stateMatrix)                  #printing our state guess after the time step
        print('\n')
        print('-' * 20)
        print('\n')
        
    print(fil.stateErrors) #printing the final uncertanties
    print() 
    print(actualStates[-1]) #printing the final real state
    
    time = [x for x in range(0, 19)] #making a time variable for plotting
    plt.plot(time, measurements, label= "measured states") #plotting the "actual state", estimated state, and measurements to compare them
    plt.plot(time, actualStates, label= "actual state")
    plt.plot(time, states, label= "estimated states")
    plt.xlabel("Time(s)")
    plt.ylabel("State(m)")
    plt.legend(loc = "upper left")
    plt.show()
