import time
import threading
import random

#this controller can run as part of a program where the functions to calculate error and output are called regualrly or can be used as a thread
#if used as a thread you must feed it a function to calculate the current state
#in the case of using a thread, you can feed it a function to adjust outputs of the system or just read the calculated outputs from the output member of the PID instance

class PID(threading.Thread):                

    def __init__(self, desiredState, pro = 0, integral = 0, deriv = 0, constants = None): #constants can be fed in one at a time, or as an array, otherwise it only needs teh desired state

        
        #just setting up all the constants either through an array, or fed in one by one
        if constants:
            self.proConstant = constants[0]
            self.intConstant = constants[1]
            self.derConstant = constants[2]
        else:
            self.proConstant = pro
            self.intConstant = integral
            self.derConstant = deriv

        self.desiredState = desiredState
        self.integral = 0                   #keeps track of the integral error acumlation
        self.lastError = 0                  #used for the derivative term
        self.lastTime = time.time()         #time since last update, used for time dependant terms like derivative and integral
        self.changed = False                #used if a new desired state is set to avoid 
        self.output = 0                     #holds our calculated output
        
        super(PID, self).__init__() #enabling thread functionality

    def run(self, getState, adjustState = None, delay = 0):     
        while True:
            state = getState()                                      #this function must be made by the user
            self.output = self.calcOutput(state)
            if adjustState:                                         #this, if used, must also be made by the user
                adjustState(self.output)
                
            time.sleep(delay)
    
    def calcError(self, state):                                                                         
        return self.desiredState - state
 

    def calcProportional(self, error):
        return self.proConstant * error

    def calcIntegral(self, error):
        self.integral += self.intConstant * error * (time.time() - self.lastTime)    
        return self.integral

    def calcDerivative(self, error):
        if self.changed:
            error = self.lastError
        return self.derConstant * (error - self.lastError) / (time.time() - self.lastTime)

    def calcOutput(self, state):            #runs through and calculates our three PID terms and sums them to generate the output
        error = self.calcError(state)
        #print("Error: " + str(error))
        pro = self.calcProportional(error)
        #print("Proportional: " + str(pro))
        integral = self.calcIntegral(error)
        #print("Integral: " + str(integral))
        deriv = self.calcDerivative(error)
        #print("Derivative: " + str(deriv))
        self.lastError = error
        self.lastTime = int(round(time.time()))
        #print("Output: " + str(pro + integral + deriv))
        #print("lastTime: " + str(self.lastTime), end= '\n\n\n')
        if self.changed:
            self.changed = False
        self.output = pro + integral + deriv
        return self.output
    
    def changeState(self, newState): #used for changing the desired state
        self.desiredState = newState
        self.changed = True


###test code below here###
def generateState():
    sign = -1 ** (random.randint(0,1))
    adjust = random.random() * 2
    generateState.state += adjust * sign
    return generateState.state

generateState.state = 10

#decomment the print statements in the class for extra debug info
if __name__ == "__main__":
    controller = PID(10,0, constants = [1,1,.5])

    while True:
        state = int(input("State Measurement: "))
        print(controller.calcOutput(state))
                
