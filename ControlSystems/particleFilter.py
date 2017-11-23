import gaussian
import random

class ParticleFilter():

    def __init__(self, bounds, prob, move, bounded = True, cyclic = False):
        self.bounds = bounds
        self.sense = sense
        self.prob = prob
        self.move = move
        self.bounded = bounded
        se;f.cyclic = cyclic
        
        self.initSample()

    def initSample(self):
        self.particles = []
        for n in range(self.numParticles):
            if isinstance(bounds[0], int):
                self.particles.append([round(x * random.random(), 3) for x in self.bounds])
            elif isinstance(bounds[0], list):
                self.particles.append([round(x[1] - x[0] * random.random + x[0], 3) for x in self.bounds])        
                    
    def calculateWeights(self, sensed):
        total = 0
        scores = []
        for particle in self.particles:
            score = self.prob(particle, sensed)
            scores.append(score)
            total += score
        weights = [x / total for x in scores]
        return weights

    def measurementUpdate(self, sensed):
        weights = self.calculateWeights(sensed)
        newParticles = []
        for n in range(self.numParticles):
            beta = max(weights) * 2
            choice = random.randint(0, self.numParticles):
            while weights[choice] < beta:
                beta -= weights[choice]
                choice += 1
            newParticles.append(self.particles[choice])
            
    def movementUpdate(self, move, sensed = None):
        moved = []
        for particle in self.particles:
            newParticle = self.move(particle)
            for x in newParticle
            moved.append(newParticle)
        self.particles = moved

        if self.bounded:
            for particle in self.particles:
                if isinstance(bounds[0], int):
                    for i, bound in enumerate(bounds):
                        if particle[i] < 0:
                            if self.cyclic:
                                particle[i] += bound
                            else:
                                particle[i] = 0
                        elif particle[i] > bound:
                            if self.cyclic:
                                particle[i] -= bound
                            else:
                                particle[i] = bound
                                
                elif isinstance(bounds[0], list):
                    for i, bound in enumerate(bounds):
                        if particle[i] < bound[0]:
                            if self.cyclic:
                                particle[i] += bound[1] - bound[0]
                            else:
                                particle[i] = bound[0]
                        elif particle[i] > bound[1]:
                            if self.cyclic:
                                particle[i] -= bound[1] - bound[0]
                            else:
                                particle[i] = bound[1]
                                
        if sensed:
            self.measurementUpdate(sensed)

    def __str__(self):
        return str(self.particles)

####EVERYTHING BELOW HERE IS JUST TEST CODE TO MAKE SURE IT IS WORKING####

realCoordinates = [4, 10]
velocities = [2, 5]
noiseMag = 2
def sense():
    mult = random.randint(-1, 1)
    while mult == 0:
        mult = random.randint(-1,1)
    fakeCoordinates = [realCoordinates[0] + noiseMag * random.random() * mult, realCoordinates[1] + noiseMag * random.random() * mult]
    fakeVelocity = [velocites[0] + noiseMag * random.random() * mult, velocity[1] + noiseMag * random.random() * mult]
    return fakeCoordinates, velocity 

def prob():
    
    
if __name__ == "__main__":
    filt = ParticleFilter([100,100])
    filt.initSample()
    print(filt)
