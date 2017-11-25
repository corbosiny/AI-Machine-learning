from __future__ import division
from math import sqrt
class FeatureScaler():

    def featureScaleRange(features):
        minFeature = min(features)
        maxFeature = max(features)

        newFeatures = [(feature - minFeature) / (maxFeature - minFeature) for feature in features]
        return newFeatures
        

    def featureScaleMean(features):
        mean = sum(features) / len(features)
        minFeature = min(features)
        maxFeature = max(features)

        newFeatures = [(feature - mean) / (maxFeature - minFeature) for feature in features]
        return newFeatures

    def featureScaleZ(features):
        mean = sum(features) / len(features)
        squaredMean = sum([feature ** 2 for feature in features]) / len(features)
        stdDev = sqrt(squaredMean - mean ** 2)
        
        zScores = [(feature - mean) / stdDev for feature in features]
        return zScores

if __name__ == "__main__":
    nums = [1,2,3,4,5]
    print(FeatureScaler.featureScaleZ(nums))
    print(nums)
