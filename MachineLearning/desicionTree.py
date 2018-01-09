from question import Question
from desicionNode import DesicionNode
from leafNode import Leaf

class DesicionTree():

    def __init__(self, trainingData, labels):

        self.columnLables = labels
        self.trainingData = trainingData
        
        self.rootNode = self.createTree(self.trainingData)


    def createTree(self, trainingData):
        if len(trainindData) == 0:
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
            values = set([dataPoint[column] for dataPoint in self.trainingData])

            for value in values:
                question = Question(column, value)
                trueSet, falseSet = DesicionTree.splitDataByQuestion(trainingData, question)
                gain = self.infoGain(trueSet, falseSet, currentUncertanty)

                if gain > bestGain:
                    bestQuestion = question

        return bestQuestion, bestGain

    def gini(self, dataSet):
        allLabelInstances = [dataPoint[-1] for dataPoint in dataSet]
        labelCounts = {label : allLabelInstances.count(label) for label in self.columnLabels}
        impurity = 1
        for label in labels:
            probability = labelCounts[label] / float(len(dataSet))
            impurity -= probability ** 2
            
        return impurity
    
    def infoGain(self, trueSet, falseSet, currentUncertanty):
        prob = float(len(trueSet)) / (len(trueSet) + len(falseSet))
        return currentUncertanty - prob * self.gini(trueSet) - (1 - prob) * self.gini(falseSet)

    def splitDataByQuestion(trainingData, question):
        trueSet, falseSet = []

        for dataPoint in trainingData:
            if question.evaluate(dataPoint):
                trueSet.append(dataPoint)
            else:
                falseSet.append(dataPoint)
        
        return trueSet, falseSet
        
    
    def predict(self, point):
        currentNode = self.rootNode
        while isinstance(currentNode, DesicionNode):
            if currentNode.question.evaluate(point):
                currentNode = currentNode.trueNode
            else:
                currentNode = currentNode.falseNode

        if currentNode is None:
            return None

        return currentNode.predict()

if __name__ == "__main__":
    trainingData = [['Green', 3, 'Apple'], ['Yellow', 3, 'Apple'], ['Red', 1, 'Grape'], ['Red', 1, 'Grape'], ['Yellow', 3, 'Lemon']]
    labels = ['color', 'diameter', 'label']
    tree = DesicionTree(trainingData, labels)

    
