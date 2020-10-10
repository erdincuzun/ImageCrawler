import os
import pandas as pd
import random

from sklearn import preprocessing 

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.metrics import log_loss

from sklearn import svm

# 150 web sites for training 50 web sites for testing - features and classification

def classification():
    train, test = flat_train_test_df()

    X_train, y_train = train.drop('relevantImg', axis=1), train['relevantImg']
    X_test, y_test = test.drop('relevantImg', axis=1), test['relevantImg']
    names = ["AdaBoost", "Random Forest", "Decision Tree", "RBF SVM", "Nearest Neighbors", "Neural Net", 
         "Naive Bayes", "ADA-RF"]
    classifiers = [
    KNeighborsClassifier(weights='distance'),
    AdaBoostClassifier(),
    RandomForestClassifier(),
    DecisionTreeClassifier(),
    SVC(),    
    MLPClassifier(),
    GaussianNB(),
    AdaBoostClassifier(RandomForestClassifier()),
    ]

    for name, clf in zip(names, classifiers):
        clf = clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        # prediction
        calculate_res(y_test, y_pred, name, "All web sites")
    return

def calculate_res(y, pred, test_name, theWebsite):
    tn, fp, fn, tp = confusion_matrix(y,  pred).ravel()
    logL = log_loss(y,  pred)
    acc, recall, pre, fmeasure = (tn+tp)/(tn + fp + fn + tp), (tp)/(fn + tp), (tp)/(fp + tp), (2*tp) / (2*tp + fp + fn)
    print('{} {}: Accuracy={} Recall={} Precision={} F-Measure={} logLoss={} '.format(test_name ,theWebsite, acc, recall, pre, fmeasure, logL))
 
def flat_train_test_df():
    df = pd.read_csv('train_image_csv.csv', sep=',')
    le = preprocessing.LabelEncoder()
    le.fit(df['fileext'].astype(str))
    df['fileext'] = le.transform(df['fileext'])
    le.fit(df['parent1tag'].astype(str))
    df['parent1tag'] = le.transform(df['parent1tag'])
    le.fit(df['parent2tag'].astype(str))
    df['parent2tag'] = le.transform(df['parent2tag'])

    dft = pd.read_csv('test_image_csv.csv', sep=',')
    le = preprocessing.LabelEncoder()
    le.fit(dft['fileext'].astype(str))
    dft['fileext'] = le.transform(dft['fileext'])
    le.fit(dft['parent1tag'].astype(str))
    dft['parent1tag'] = le.transform(dft['parent1tag'])
    le.fit(dft['parent2tag'].astype(str))
    dft['parent2tag'] = le.transform(dft['parent2tag'])
   
    return df, dft


classification()


