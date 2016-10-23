from sklearn.svm import SVC

features =  [[1,1], [2,2], [3,3], [.5,.75], [.3,.1]]
labels = [1,2,2,1,1]

clf = SVC(kernel = 'linear', C= 1) #kernel decides shape of desicion boundary, #c forces it get more correct, still messing with gamma
clf.fit(features, labels)
print(clf.predict([[1.5,1.5], [2,7]]))
