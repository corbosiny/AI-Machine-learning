from desicionTree import DesicionTree

class DesicionTreeTester():

    def __init__(self):
        pass

    def test(self, testingData, labels):
        self.testingTree = DesicionTree(trainingData, labels)
        numCorrect = len([dataPoint for dataPoint in trainingData if self.testingTree.predictModelOutput(dataPoint[:-1]) == dataPoint[-1]])
        print("Score: ", numCorrect / len(testingData))
        #assert(self.testingTree.predict(testingData[0][:-1]) == testingData[0][-1])
        
if __name__ == "__main__":
    trainingData = [['Green', 3, 'Apple'], ['Yellow', 3, 'Apple'], ['Red', 1, 'Grape'], ['Red', 1, 'Grape'], ['Yellow', 3, 'Lemon']]
    labels = ['color', 'diameter', 'label']
    tester = DesicionTreeTester()

    tester.test(trainingData, labels)
