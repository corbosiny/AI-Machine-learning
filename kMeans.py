import random
from scipy.spatial import distance
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cross_validation import train_test_split

class KMeans():

    colors = ['blue', 'red', 'black', 'green', 'yellow' , 'cyan', 'orange', 'purple'] #order of colors that will be assigned to the clusters, if more than this random colors will be assigned
    def __init__(self, data, numMeans = 2, featureScaling = False):
        self.data = data
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
                    self.data[j][i] = (self.data[j][i] - rang[0]) / rang[1]
                except ZeroDivisionError:
                    self.data[j][i] = 0
                    
            for j in range(self.numMeans):              #feature scaling the means
                try:
                    self.means[j][i] = (self.means[j][i] - rang[0]) / rang[1]
                except ZeroDivisionError:
                    self.means[j][i] = 0

        
    def displayData(self, nearest= None):       #graphs all the data
        if nearest == None:                     #neads the data split into clusters, if not provided it will calculate them
            nearest = self.calcNearest()

        if len(self.ranges) > 2:                #setup up for 3D graphs if the number of dimensions is greater than 2         
            fig1 = plt.figure()
            ax1 = fig1.add_subplot(111, projection='3d')
            
        for cluster in nearest:                 #going through each cluster
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
                ax1.scatter(parameters[0], parameters[1], parameters[2], color= clusterColor, label= "Cluster %d" % nearest.index(cluster))
                ax1.scatter(self.means[nearest.index(cluster)][0], self.means[nearest.index(cluster)][1], self.means[nearest.index(cluster)][2], color= clusterColor, marker= "x", label= "Mean %d" % nearest.index(cluster))
            else:                           #otherwise we do a 2D scatter plot
                plt.scatter(parameters[0], parameters[1], color= clusterColor, label= "Cluster %d" % nearest.index(cluster))
                plt.scatter(self.means[nearest.index(cluster)][0], self.means[nearest.index(cluster)][1], color= clusterColor, marker= "x", label= "Mean %d" % nearest.index(cluster))

        plt.legend(loc='upper left', shadow=True)
        plt.show()


    def randomColor():  #generates a random RGB value stored in an array
        return [random.random(), random.random(), random.random()]


    def calcNearest(self):                  #seperates data into clusters based on how close they are to each random mean
        nearest = [[] for x in self.means]
        for point in self.data:     #going through each data point
            distances = []
            for centroid in self.means:                                 #finding the closest mean
                distances.append(distance.euclidean(centroid, point))
                
            minDistance = min(distances)
            nearest[distances.index(minDistance)].append(point) #appending this data point to the cluster list of the closest mean
            
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
        for mean in self.means:
            distances.append(distance.euclidean(mean, point))

        clusterIndex = distances.index(min(distances))
        return 'Cluster: %d' % clusterIndex



    def fit(self, numLoops = 100):          #runs through fitting the clusters
        nearest = self.calcNearest()
        self.change = False
        
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
            if not self.change:
                return


###Test Code Below Here###
if __name__ == "__main__":
    #fakeData = [[5,5],[0,1],[5,7],[6,5],[6,4], [0,0], [1,1], [2,1.5], [2,4], [2.5,4], [2.2,3.6]]
    #means = KMeans(fakeData, 3)
    irisData = datasets.load_iris()
    Xset,Xtest, Yset, Ytest = train_test_split(irisData.data, irisData.target, test_size = .20)
    means = KMeans(Xset, 3, featureScaling = True)
    means.fit()
    means.displayData()
    #print(means.predict([0,0]))
