from __future__ import division
from question import Question
from desicionNode import DesicionNode
from leafNode import Leaf

class DesicionTree():

    def __init__(self, trainingData, labels):

        self.columnLables = labels
        self.trainingData = trainingData
        
        self.rootNode = self.createTree(self.trainingData)


    def createTree(self, trainingData):
        if len(trainingData) == 0:
            return None
        
        question, gain = self.findBestQuestion(trainingData)
        if gain == 0:
            return Leaf(trainingData)
        
        trueSet, falseSet = DesicionTree.splitDataByQuestion(trainingData, question)

        trueBranch = self.createTree(trueSet)
        falseBranch = self.createTree(falseSet)
        return DesicionNode(question, trueBranch, falseBranch) 

    def findBestQuestion(self, trainingData):
        bestQuestion = None
        bestGain = 0
        currentUncertainty = self.gini(trainingData)
        
        for column in range(len(trainingData[0]) - 1):
            values = set([dataPoint[column] for dataPoint in trainingData])

            for value in values:
                question = Question(column, value)
                trueSet, falseSet = DesicionTree.splitDataByQuestion(trainingData, question)

                if len(falseSet) == 0 or len(trueSet) == 0:
                    continue
                
                gain = self.infoGain(trueSet, falseSet, currentUncertainty)

                if gain > bestGain:
                    bestQuestion = question
                    bestGain = gain

        return bestQuestion, bestGain

    def gini(self, dataSet):
        allLabelInstances = [dataPoint[-1] for dataPoint in dataSet]
        setOfLabels = set(allLabelInstances)
        labelCounts = {label : allLabelInstances.count(label) for label in setOfLabels}
        impurity = 1.0
        for label in setOfLabels:
            probability = labelCounts[label] / float(len(dataSet))
            impurity -= probability ** 2
        return impurity
    
    def infoGain(self, trueSet, falseSet, currentUncertainty):
        prob = float(len(trueSet)) / (len(trueSet) + len(falseSet))
        return currentUncertainty - prob * self.gini(trueSet) - (1 - prob) * self.gini(falseSet)

    def splitDataByQuestion(trainingData, question):
        trueSet, falseSet = [], []

        for dataPoint in trainingData:
            if question.evaluate(dataPoint):
                trueSet.append(dataPoint)
            else:
                falseSet.append(dataPoint)
        
        return trueSet, falseSet
        
    
    def predictModelOutput(self, point):
        currentNode = self.rootNode
        while isinstance(currentNode, DesicionNode):
            if currentNode.question.evaluate(point):
                currentNode = currentNode.trueNode
            else:
                currentNode = currentNode.falseNode
            

        if currentNode is None:
            return None
        return currentNode.predict()

    def predict(self, dataset):
        predictions = [self.predictModelOutput(dataPoint) for dataPoint in dataset]
        return predictions

if __name__ == "__main__":
    trainingData = [['Green', 3, 'Apple'], ['Yellow', 3, 'Apple'], ['Red', 1, 'Grape'], ['Red', 1, 'Grape'], ['Yellow', 3, 'Lemon']]
    labels = ['color', 'diameter', 'label']
    tree = DesicionTree(trainingData, labels)
    tree.predictModelOutput(trainingData[0])

    
