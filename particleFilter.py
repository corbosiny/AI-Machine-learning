import gaussian
import random

class ParticleFilter():

    def __init__(self, bounds, sense, prob, move = None):
        self.bounds = bounds
        self.sense = sense
        self.prob = prob
        self.move = move

        self.initSample()

    def initSample(self):
        self.particles = []
        for n in range(self.numParticles):
            self.particles.append([round(x * random.random(), 3) for x in self.bounds])
        self.sensed = self.sense()
    
    def calculateWeights(self):
        total = 0
        scores = []
        for particle in self.particles:
            score = self.prob(particle, self.sensed)
            scores.append(score)
            total += score
        weights = [x / total for x in scores]
        return weights

    def resample(self):
        weights = self.calculateWeights()
        newParticles = []
        for n in range(self.numParticles):
            beta = max(weights) * 2
            choice = random.randint(0, self.numParticles):
            while weights[choice] < beta:
                beta -= weights[choice]
                choice += 1
            newParticles.append(self.particles[choice])
        self.particles = newPatricles

        if self.move:
            moved = []
            for particle in self.particles:
                newParticle = self.move(particle)
                moved.append(newParticle)
            self.particles = moved
            

    def __str__(self):
        return str(self.particles)

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
