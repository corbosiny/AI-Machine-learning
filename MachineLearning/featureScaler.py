from __future__ import division
from math import sqrt
class FeatureScaler():

    def __init__(self, features):
        self.features = features
    
    def featureScaleRange(self):
        self.minFeature = min(self.features)
        self.maxFeature = max(self.features)

        newFeatures = [self.featureScaleRangePoint(feature) for feature in self.features]
        return newFeatures

    def featureScaleRangePoint(self, datapoint):
        return (datapoint - self.minFeature) / (self.maxFeature - self.minFeature)

    def featureScaleMean(self):
        self.mean = sum(self.features) / len(self.features)
        self.minFeature = min(self.features)
        self.maxFeature = max(self.features)

        newFeatures = [self.featureScaleMeanPoint(feature) for feature in self.features]
        return newFeatures

    def featureScaleMeanPoint(self, datapoint):
        return (datapoint - self.mean) / (self.maxFeature - self.minFeature) 

    def featureScaleZ(self):
        self.mean = sum(self.features) / len(self.features)
        squaredMean = sum([feature ** 2 for feature in self.features]) / len(self.features)
        self.stdDev = sqrt(squaredMean - self.mean ** 2)
        
        zScores = [self.featureScaleZPoint(feature) for feature in self.features]
        return zScores

    def featureScaleZPoint(self, datapoint):
        return (datapoint - self.mean) / self.stdDev

if __name__ == "__main__":
    nums = [1,2,3,4,5]
    scaler = FeatureScaler(nums)
    print(scaler.featureScaleRange())
    print(scaler.featureScaleMean())
    print(scaler.featureScaleZ())
    print(nums)
