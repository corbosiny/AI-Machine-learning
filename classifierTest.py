import warnings
warnings.filterwarnings("ignore")

from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from kNearestNeighbors import KNearestNeighbors <-- My classifier
from kMeans import KMeans <-- My classifier


###Just testing my classifiers versus scikit classifiers with fake data
X = [[181, 80, 44], [177, 70, 43], [160, 60, 38], [154, 54, 37], [166, 65, 40],
     [190, 90, 47], [175, 64, 39],
     [177, 70, 40], [159, 55, 37], [171, 75, 42], [181, 85, 43]]

Y = ['male', 'male', 'female', 'female', 'male', 'male', 'female', 'female',
     'female', 'male', 'male']


clfTree = tree.DecisionTreeClassifier()
clfNeighbors = KNearestNeighbors(X, Y)
clfMeans = KMeans(X, Y)
clfGaussian = GaussianNB()
clfSVM = svm.SVC()


clfTree = clfTree.fit(X, Y)
clfGaussian = clfGaussian.fit(X,Y)
clfMeans.fit()
clfSVM.fit(X, Y)

testPoint = [190, 70, 43]
print("Sklearn Classifiers:")
print("Desicion Tree", clfTree.predict(testPoint))
print("Naive Bayes: ", clfGaussian.predict(testPoint))
print("SVM: ", clfSVM.predict(testPoint))
print('-' * 25)
print("My classifiers: ")
print("K-Nearest Neighbors: ", clfNeighbors.predict(testPoint))
print("K-Means: ", clfMeans.predict(testPoint))
clfMeans.displayData()


