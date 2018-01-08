
class DesicionTree():

    def __init__(self, trainingData):

        self.lables = trainingData[0]
        self.trainingData = trainingData[1:]
        
        self.rootNode = DesicionTree.createTree(self.trainingData)


    def createTree(trainingData):

        question = DesicionTree.findBestQuestion(trainingData)
        trueSet, falseSet = DesicionTree.splitDataByQuestion(trainingData, question)

        trueBranch, falseBranch = DesicionTree.createBranches(trueSet, falseSet)
        
            
        if len(trueSet) == 0 and len(falseSet) == 0:
            return Leaf(trainingData)
        else:
            return DesicionNode(question, trueBranch, falseBranch) 
    
    def predict(self):
        pass


if __name__ == "__main__":
    pass
