import random
from scipy.spatial import distance
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

class KMeans():

    colors = ['blue', 'red', 'black', 'green', 'yellow' , 'cyan', 'orange', 'purple']
    def __init__(self, data, numMeans = 2):
        self.data = data
        self.numMeans = numMeans
        self.ranges = []
        for x in range(len(data[0])):
            vals = [y[x] for y in data]
            self.ranges.append([min(vals),max(vals)])

        self.means = [] 
        for x in range(numMeans):
            vals = []
            for y in range(len(self.ranges)):
                vals.append(random.randrange(self.ranges[y][0], self.ranges[y][1]))
                vals[y] -= random.random() * 2
                if vals[y] < self.ranges[y][0]:
                    vals[y] = abs(vals[y]) 
                vals[y] = round(vals[y], 3)            
            self.means.append(vals)

        self.splitData = []        
        for x in range(len(data[0])):
            self.splitData.append([y[x] for y in self.data + self.means])

    def displayData(self, nearest= None):
        if nearest == None:
            nearest = self.calcNearest()
        for cluster in nearest:

            parameters = [[] for i in range(len(self.ranges))]
            for param in range(len(self.ranges)):
                for point in cluster:
                    parameters[param].append(point[param])
                #parameters[param].append(self.means[nearest.index(cluster)][param])
            try:
                clusterColor = KMeans.colors[nearest.index(cluster)]
            except:
                clusterColor = KMeans.randomColor()

            plt.scatter(parameters[0], parameters[1], color= clusterColor, label= "Cluster %d" % nearest.index(cluster))
            plt.scatter(self.means[nearest.index(cluster)][0], self.means[nearest.index(cluster)][1], color= clusterColor, marker= "x", label= "Mean %d" % nearest.index(cluster))
        plt.legend(loc='upper left', shadow=True)
        plt.show()

    def randomColor():
        return [random.random(), random.random(), random.random()]

    def calcNearest(self):
        nearest = [[] for x in self.means]
        for point in self.data:
            distances = []
            for centroid in self.means:
                distances.append(distance.euclidean(centroid, point))
            minDistance = min(distances)
            nearest[distances.index(minDistance)].append(point)
            
        return nearest

    def predict(self, testData):
        if isinstance(testData[0], list):
            predictions = []
            for point in testData:
                predictions.append(self.predictDataPoint(point))
            return predictions
        else:
            return self.predictDataPoint(testData)
            

    def predictDataPoint(self, point):
        distances = []
        for mean in self.means:
            distances.append(distance.euclidean(mean, point))

        clusterIndex = distances.index(min(distances))
        return 'Cluster: %d' % clusterIndex

    def fit(self):
        nearest = self.calcNearest()
        self.displayData(nearest)
        self.change = False
        while True:
            self.change = False
            averages = [[] for i in range(len(nearest))]
            for num, cluster in enumerate(nearest):
                for param in range(len(self.ranges)):
                    total = [point[param] for point in cluster]
                    #print(total)
                    try:
                        average = sum(total) / len(total)
                    except:
                        print(self.ranges)
                        average = random.randrange(self.ranges[param][0], self.ranges[param][1])
                        average -= random.random()
                    #print(average)
                    averages[num].append(average)

            for i in range(len(self.means)):
                if self.means[i] != averages[i]:
                    self.change = True
                    self.means[i][0] = averages[i][0] + 0
                    self.means[i][1] = averages[i][1] + 0
            #input('>>')
            nearest = self.calcNearest()
            #self.displayData(nearest)
            if not self.change:
                return

if __name__ == "__main__":
    fakeData = [[5,5],[0,1],[5,7],[6,5],[6,4], [0,0], [1,1], [2,1.5], [2,4], [2.5,4], [2.2,3.6]]
    means = KMeans(fakeData, 3)
    means.fit()
    means.displayData()
    print(means.predict([0,0]))
