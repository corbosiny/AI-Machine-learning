class DesicionNode():

    def __init__(self, question, trueNode, falseNode):
        self.question = question
        self.trueNode = trueNode
        self.falseNode = falseNode


    def __repr__(self):
        return str(self.question)
    
if __name__ == "___main__":
    from question import Question
    question = Question()
    trueNode = None
    falseNode = None

    testNode = DesicionNode(question, trueNode, falseNode)
