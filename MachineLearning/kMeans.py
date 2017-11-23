import warnings
warnings.filterwarnings("ignore")
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")

import random
import scipy
from scipy.spatial import distance
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cross_validation import train_test_split

class KMeans():

    colors = ['blue', 'red', 'black', 'green', 'yellow' , 'cyan', 'orange', 'purple'] #order of colors that will be assigned to the clusters, if more than this random colors will be assigned
    def __init__(self, data, labels = None, allLabels = None, numMeans = 2, featureScaling = False):
        self.data = data

        self.labels = labels
        if labels is not None:
            if allLabels:
                self.allLabels = allLabels
            else:
                allLabels = []
                for label in self.labels:
                    if label not in allLabels:
                        allLabels.append(label)
                self.allLabels = allLabels
                
        self.numMeans = numMeans
        self.featureScaling = featureScaling
        self.ranges = []
        
        for x in range(len(data[0])):  #calculating all the ranges of each feature set, used for feature scaling
            vals = [y[x] for y in data]
            self.ranges.append([min(vals),max(vals)])


        self.means = []
        for x in range(numMeans):                           #calculates random means within the feature ranges
            vals = []
            for y in range(len(self.ranges)):
                vals.append(random.randrange(int(self.ranges[y][0]), int(self.ranges[y][1])))
                vals[y] -= random.random() * 2
                
                while vals[y] < self.ranges[y][0] or vals[y] > self.ranges[y][1]:  #keeping picking a mean until we are in the range of the feature
                    if vals[y] < self.ranges[y][0]:
                        vals[y] = random.randrange(int(self.ranges[y][0]), int(self.ranges[y][1])) - random.random()
           
            self.means.append(vals)

        if featureScaling:
            self.featureScale()

        self.splitData = []             #not used as of now, splits each set of features into its own array for easy viewing
        for x in range(len(data[0])):
            self.splitData.append([y[x] for y in self.data])



    def featureScale(self):                    #turns all feeatures into a number between zero and one
        for i, rang in enumerate(self.ranges): #going through each feature
            
            for j in range(len(self.data)):             #feature scaling the data point feature
                try:
                    self.data[j][i] = (self.data[j][i] - rang[0]) / (rang[1] - rang[0])
                except ZeroDivisionError:
                    self.data[j][i] = self.ranges[i][0]
                    
            for j in range(self.numMeans):              #feature scaling the means
                try:
                    self.means[j][i] = (self.means[j][i] - rang[0]) / (rang[1] - rang[0])
                except ZeroDivisionError:
                    self.means[j][i] = self.ranges[i][0]

        
    def displayData(self, nearest= None, clusterLabels = None):       #graphs all the data
        if nearest == None:                     #neads the data split into clusters, if not provided it will calculate them
            nearest = self.calcNearest()

        if len(self.ranges) > 2:                #setup up for 3D graphs if the number of dimensions is greater than 2         
            fig1 = plt.figure()
            ax1 = fig1.add_subplot(111, projection='3d')
            
        for i, cluster in enumerate(nearest):                 #going through each cluster
            parameters = [[] for i in range(len(self.ranges))]
            for param in range(len(self.ranges)):
                for point in cluster:
                    parameters[param].append(point[param])
                #parameters[param].append(self.means[nearest.index(cluster)][param])

            try:            #coloring the cluster
                clusterColor = KMeans.colors[nearest.index(cluster)]
            except:
                clusterColor = KMeans.randomColor()
                
            if len(self.ranges) > 2:        #if doing 3D graphs then we use the ax1 object we set up
                if self.labels is not None:
                    ax1.scatter(parameters[0], parameters[1], parameters[2], color= clusterColor, label= self.clusterLabels[i])
                else:
                    ax1.scatter(parameters[0], parameters[1], parameters[2], color= clusterColor, label= "Cluster %d" % nearest.index(cluster))
                ax1.scatter(self.means[nearest.index(cluster)][0], self.means[nearest.index(cluster)][1], self.means[nearest.index(cluster)][2], color= clusterColor, marker= "x", label= "Mean %d" % nearest.index(cluster))
            else:                           #otherwise we do a 2D scatter plot
                if self.labels is not None:
                    plt.scatter(parameters[0], parameters[1], color= clusterColor, label= self.clusterLabels[i])
                else:
                    plt.scatter(parameters[0], parameters[1], color= clusterColor, label= "Cluster %d" % nearest.index(cluster))
                plt.scatter(self.means[nearest.index(cluster)][0], self.means[nearest.index(cluster)][1], color= clusterColor, marker= "x", label= "Mean %d" % nearest.index(cluster))
                
        plt.legend(loc='upper left', shadow=True)
        plt.show()


    def randomColor():  #generates a random RGB value stored in an array
        return [random.random(), random.random(), random.random()]


    def calcNearest(self):                  #seperates data into clusters based on how close they are to each random mean
        nearest = [[] for x in self.means]
        nearestLabels = [[] for x in self.means] 
        for i, point in enumerate(self.data):     #going through each data point
            distances = []
            for centroid in self.means:                                 #finding the closest mean
                distances.append(distance.euclidean(centroid, point))
                
            minDistance = min(distances)
            nearest[distances.index(minDistance)].append(point) #appending this data point to the cluster list of the closest mean
            if self.labels is not None:
                nearestLabels[distances.index(minDistance)].append(self.labels[i])

        if self.labels is not None:
            self.clusterLabels = []
            for cluster in range(self.numMeans):
                labelCount = [nearestLabels[cluster].count(label) for label in self.allLabels]
                self.clusterLabels.append(self.allLabels[labelCount.index(max(labelCount))])
                
        return nearest

    def predict(self, testData):            #makes group predictions if list is put in
        if isinstance(testData[0], list):
            predictions = []
            for point in testData:
                predictions.append(self.predictDataPoint(point))
            return predictions
        else:
            return self.predictDataPoint(testData)
            

    def predictDataPoint(self, point):      #finds closest mean, returns that cluser number
        distances = []
        
        if self.featureScaling:         #if feature scaling has been done, we have to feature scale the test inputs as well
            for i in range(len(self.ranges)):
                try:
                    point[i] = (point[i] - self.ranges[i][0]) / (self.ranges[i][1] - self.ranges[i][0])
                except ZeroDivisionError:
                    point[i] = self.ranges[i][0]
                    
        for mean in self.means:
            distances.append(distance.euclidean(mean, point))

        clusterIndex = distances.index(min(distances))
        
        return self.clusterLabels[clusterIndex]


    def scoreTest(self, testData, answers):         #for testing the accuracy of the classifier
        total = 0
        for i in range(len(testData)):
            if self.predictDataPoint(testData[i]) == answers[i]:
                total += 1
                
        return total / float(len(answers))


    def fit(self, numLoops = 100):          #runs through fitting the clusters
        nearest = self.calcNearest()
        
        for y in range(numLoops):
            averages = [[] for i in range(len(nearest))]    #holds the average of each cluster
            for num, cluster in enumerate(nearest):         #going through each cluster
                for param in range(len(self.ranges)):
                    total = [point[param] for point in cluster]     #collecting all the datapoint values of that feature and averaging them
                    try:
                        average = sum(total) / len(total)
                    except:
                        average = random.randrange(int(self.ranges[param][0]), int(self.ranges[param][1])) #if there are no points in that cluster we re-initialize that mean 
                        average -= random.random()
                    averages[num].append(average)

            for i in range(len(self.means)):
                self.means[i][0] = averages[i][0] + 0  #updating the means
                self.means[i][1] = averages[i][1] + 0
                
            #input('>>')
            nearest = self.calcNearest()    #updating nearest
            #self.displayData(nearest)
        return

###Test Code Below Here###
if __name__ == "__main__":

    fakeData = [[1,1,1],[1.4,.7,.3],[12,7,11],[0,-1,2],[10,9,8],[7,16,12],[7,6,5]]

    irisData = datasets.load_iris()
    Xset,Xtest, Yset, Ytest = train_test_split(irisData.data, irisData.target, test_size = .75)
    labels = []

    means = KMeans(Xset, labels= Yset, allLabels = [0,1,2], numMeans= 3, featureScaling = True)
    means.fit(500)
    print(means.predictDataPoint(Xtest[0]))
    print(means.scoreTest(Xtest, Ytest))
    means.displayData()
