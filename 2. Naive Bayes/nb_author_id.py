#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 1 (Naive Bayes) mini-project. 

    Use a Naive Bayes Classifier to identify emails by their authors
    
    authors and labels:
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score



### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###
clf = GaussianNB()

#train the classifer
t0 = time()
clf.fit(features_train, labels_train)
print("NB Training time: " + str(round(time()-t0,3)) + " s")

#ask classifier to predict
t0 = time()
labels_pred = clf.predict(features_test)
print("NB Prediction time: " + str(round(time()-t0,3)) + " s")

print("NB Predicted labels: " + str(labels_pred))
print("NB Accuracy: " + str(accuracy_score(labels_test, labels_pred)))
#########################################################


