import random
import numpy as np

mutateRate = 0.04
populationSize = 200
targetPhrase = 'programming is fun!'

def setup():
    global populationSize
    global targetPhrase
    population = []

    for x in range(populationSize):
        newWord = ''
        for y in range(len(targetPhrase)):
            newChr = chr(random.randint(32, 122))
            newWord += newChr
            
        population.append(newWord)

    return population

def calcFitness(population):
    global targetPhrase
    fitnessScores = []

    l = len(targetPhrase)
    for x in population:
        score = sum([x == y for x,y in zip(x, targetPhrase)]) / l
        fitnessScores.append(score)

    return fitnessScores

def breed(population, fitnessScores):
    global populationSize
    totalFitness = sum(fitnessScores)
    if totalFitness == 0:
        totalFitness = 1
        
    newGeneration = []

    adjustedFitnesses = [x / totalFitness for x in fitnessScores]
    if sum(adjustedFitnesses) == 0:
        adjustedFitnesses = [1.0 / len(fitnessScores) for x in fitnessScores]


    for x in range(populationSize):
        parents = np.random.choice(population, 2, p = adjustedFitnesses)

        child = crossOver(parents[0], parents[1])
        newGeneration.append(child)
        
    return newGeneration

def crossOver(parent1, parent2):
    global targetPhrase
    child = ''
    
    length = len(parent1)

##    for x in range(length):
##        child += np.random.choice([parent1[x], parent2[x]], 1, p = [.5,.5])[0]

    child = parent1[0:int(length/2)] + parent2[int(length/2):]

##    for x in range(length):
##        if parent1[x] == targetPhrase[x]:
##            child += parent1[x]
##
##        elif parent2[x] == targetPhrase[x]:
##            child += parent2[x]
##
##        else:
##            child += np.random.choice([parent1[x], parent2[x]], 1, p = [.5,.5])[0]

    child = mutate(child)

    return child

def mutate(child):
    global mutateRate

    muChild = ''
    for x in range(len(child)):
        if random.random() <= mutateRate:
            muChild += chr(random.randint(32, 122))
        else:
            muChild += child[x]
            
    return muChild


def geneticAlgorithm():
    global targetPhrase
    population = setup()
    while targetPhrase not in population:
        scores = calcFitness(population)
        print(population[scores.index(max(scores))])
        population = breed(population, scores)

    scores = calcFitness(population)
    print(population[scores.index(max(scores))])
    
if __name__ == '__main__':
    geneticAlgorithm()
