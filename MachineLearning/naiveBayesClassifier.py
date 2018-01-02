import pandas as pd
import csv
from dataSplitter import DataSplitter
from gaussian import Gaussian

class NaiveBayesClassifier():

    def __init__(self, trainingSet):
        self.trainingSet = trainingSet
        self.atributesByClass = []

    def seperateDataByClass(dataset):
        seperatedDataByClass = {}
        for dataPoint in dataset:
            try:
                seperatedDataByClass[dataPoint[-1]].append(dataPoint)
            except:
                seperatedDataByClass[dataPoint[-1]] = []
                seperatedDataByClass[dataPoint[-1]].append(dataPoint)
                
        return seperatedDataByClass


    def fit(self):
        self.dataSplitByClass = NaiveBayesClassifier.seperateDataByClass(self.trainingSet)
        self.featureDistributionsByClass = {}
        self.classProbabilities = {}
        
        for label in self.dataSplitByClass:
            self.featureDistributionsByClass[label] = NaiveBayesClassifier.generateFeatureDistributions(self.dataSplitByClass[label])
            self.classProbabilities[label] = NaiveBayesClassifier.calculateClassProbability(label, self.trainingSet)
            

    def generateFeatureDistributions(labelSet):
        distributions = []
        for featureNum in range(len(labelSet[0]) - 1):    #-1 to leave off the label on the end
            featureSet = [datapoint[featureNum] for datapoint in labelSet]
            mean = sum(featureSet) / len(featureSet)
            variance = sum([(feature - mean) ** 2 for feature in featureSet]) / len(featureSet)
            normalDistributionOfFeature = Gaussian(variance, mean)
            distributions.append(normalDistributionOfFeature)
        
        return distributions

    def calculateClassProbability(label, dataset):
        labelSubset = [datapoint for datapoint in dataset if datapoint[-1] == label]
        return len(labelSubset) / len(dataset)

    def predict(self, dataPoint):
        predictionChancesByLabel = {}
        for label in self.dataSplitByClass:
            try:
                predictionChancesByLabel[label] = self.classProbabilities[label]
                distributions = self.featureDistributionsByClass[label]
                for featureNum, feature in enumerate(dataPoint):
                    if feature == None:
                        continue
                    else:
                        predictionChancesByLabel[label] *= distributions[featureNum].evaluate(feature)

            except:
                pass #if the datapoint has more data than our testing data we ignore that
                
        return NaiveBayesClassifier.calcMaxPrediction(predictionChancesByLabel)


    def calcMaxPrediction(predictionChancesByLabel):
        prediction = [0, 0]
        for label in predictionChancesByLabel:
            if predictionChancesByLabel[label] > prediction[1]:
                prediction = [label, predictionChancesByLabel[label]]
        return prediction[0]
    
    def loadCSV(fileName):
        lines = csv.reader(open(fileName, "r"))
        dataset = list(lines)
        dataset = [[float(num) for num in line] for line in dataset]
        return dataset

    
if __name__ == "__main__":
    fileName = "pima-indians-diabetes.csv"
    dataset = NaiveBayesClassifier.loadCSV(fileName)
    classifier = NaiveBayesClassifier(dataset)
    classifier.fit()
