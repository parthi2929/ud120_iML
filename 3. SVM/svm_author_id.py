#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess
from sklearn import svm
from sklearn.metrics import accuracy_score


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###
clf = svm.SVC(C=10000, kernel='rbf')


#features_train = features_train[:int(len(features_train)/100)] 
#labels_train = labels_train[:int(len(labels_train)/100)] 

#train the classifer
t0 = time()
clf.fit(features_train, labels_train)
print("SVM Training time: " + str(round(time()-t0,3)) + " s")

#ask classifier to predict
t0 = time()
labels_pred = clf.predict(features_test)
print("SVM Prediction time: " + str(round(time()-t0,3)) + " s")

print("SVM Predicted labels: " + str(len(labels_pred)))
print("SVM Accuracy: " + str(accuracy_score(labels_test, labels_pred)))

print("predicted label for {} is {}".format(10,labels_pred[10]))
print("predicted label for {} is {}".format(26,labels_pred[26]))
print("predicted label for {} is {}".format(50,labels_pred[50]))
print("Total labels predicted to be from Chris :" + str(sum(labels_pred)))
#########################################################


