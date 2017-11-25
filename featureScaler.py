from __future__ import division
from math import sqrt
class FeatureScaler():

    def featureScaleRange(features):
        minFeature = min(features)
        maxFeature = max(features)

        scaledFeatures = [(feature - minFeature) / (maxFeature - minFeature) for feature in features]
        return scaledFeatures
        

    def featureScaleMean(features):
        mean = sum(features) / len(features)
        minFeature = min(features)
        maxFeature = max(features)

        scaledFeatures = [(feature - mean) / (maxFeature - minFeature) for feature in features]
        return scaledFeatures

    def featureScaleZ(features):
        mean = sum(features) / len(features)
        squaredMean = sum([feature ** 2 for feature in features]) / len(features)
        stdDev = sqrt(squaredMean - mean ** 2)
        
        zScores = [(feature - mean) / stdDev for feature in features]
        return zScores

    def findRatios(features):
        mean = sum(features) / len(features)
        featureRange = max(features) - min(features)
        squaredMean = sum([feature ** 2 for feature in features]) / len(features)
        stdDev = sqrt(squaredMean - mean ** 2)
    
        return mean, featureRange, stdDev
    
    def unscaleFeatures(features, scaler = 1, offset = 0):
        unscaledFeatures = [feature * scaler + offset for feature in features]
        return unscaledFeatures

    def unscaleFeaturesRange(scaledFeatures, features):
        __, featureRange, __ = FeatureScaler.findRatios(features)
        minFeature = min(features)
        return FeatureScaler.unscaleFeatures(scaledFeatures, featureRange, minFeature)

    def unscaleFeaturesMean(scaledFeatures, features):
        mean, featureRange, __ = FeatureScaler.findRatios(features)
        return FeatureScaler.unscaleFeatures(scaledFeatures, featureRange, mean)

    def unscaleFeaturesZ(scaledFeatures, features):
        mean, __, stdDev = FeatureScaler.findRatios(features)
        minFeature = min(features)
        return FeatureScaler.unscaleFeatures(scaledFeatures, stdDev, mean)


if __name__ == "__main__":
    nums = [1,2,3,4,5]
    scaledNums = FeatureScaler.featureScaleZ(nums)
    print(FeatureScaler.unscaleFeaturesZ(scaledNums, nums))

    scaledNum = FeatureScaler.featureScaleMean(nums)
    print(FeatureScaler.unscaleFeaturesMean(scaledNum, nums))

    scaledNum = FeatureScaler.featureScaleRange(nums)
    print(FeatureScaler.unscaleFeaturesRange(scaledNum, nums))
    
