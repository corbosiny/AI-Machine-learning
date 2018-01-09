class DesicionNode():

    def __init__(self, question, trueBranch, falseBranch):
        self.question = question
        self.trueBranch = trueBranch
        self.falseBranch = falseBranch


    def __repr__(self):
        return str(self.question)
    
if __name__ == "___main__":
    from question import Question
    question = Question()
    trueNode = None
    falseNode = None

    testNode = DesicionNode(question, trueNode, falseNode)
