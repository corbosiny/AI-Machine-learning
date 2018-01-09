
class Question():

    def __init__(self, columnNumber, valueToCompare):
        self.columnNumber = columnNumber
        self.valueToCompare = valueToCompare

    def evaluate(self, row):
        rowVal = row[self.columnNumber]
        if Question.isNumeric(self.valueToCompare):
            return rowVal >= self.valueToCompare
        else:
            return rowVal == self.valueToCompare
        
    def __repr__(self):
        if Question.isNumeric(self.valueToCompare):
            return "Is feature #%d >= %d ?" % (self.columnNumber, self.valueToCompare)
        else:
            return "Is feature #%d == %s ?" % (self.columnNumber, self.valueToCompare)
            
        
    def isNumeric(value):
        return isinstance(value, int) or isinstance(value, float)


if __name__ == "__main__":
    question = Question(0, 5)
    print(question)
    print(question.evaluate([5, 3]))
    print(question.evaluate([4, 2]))
    print(question.evaluate([6, 3]))
