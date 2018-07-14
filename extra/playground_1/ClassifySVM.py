def classify(features_train, labels_train):   
    ### import the sklearn module for SVM
    ### create classifier
    ### fit the classifier on the training features and labels
    ### return the fit classifier
    
        
    ### your code goes here!
    from sklearn.svm import SVC
    clf = SVC(C=100, kernel='rbf',gamma=1)
    clf.fit(features_train, labels_train)
    return clf