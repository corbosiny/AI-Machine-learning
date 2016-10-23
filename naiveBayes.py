import numpy as np
x = np.array([[-1,1], [-2,-1], [-3, -2], [1,1], [2,1], [3,2]])
y = np.array([1,1,1,2,2,2])

from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(x,y)
GaussianNB()
print(clf.predict([[-.8, -1], [2,1]]))

#clf.score(features, labels_test) <- calculates how accurate it is at classifiying
