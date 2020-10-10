import os
import pandas as pd
import random

from sklearn import preprocessing 

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.metrics import log_loss

from sklearn import svm

# 150 web sites for training 50 web sites for testing - features and classification

def classification(dropFeatures = []):
    train, test = flat_train_test_df(dropFeatures)

    X_train, y_train = train.drop('relevantImg', axis=1), train['relevantImg']
    X_test, y_test = test.drop('relevantImg', axis=1), test['relevantImg']

    clf = AdaBoostClassifier()
    clf = clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    # prediction
    calculate_res(y_test, y_pred, "Adaboost", "All web sites")
        
    return

def calculate_res(y, pred, test_name, theWebsite):
    tn, fp, fn, tp = confusion_matrix(y,  pred).ravel()
    logL = log_loss(y,  pred)
    acc, recall, pre, fmeasure = (tn+tp)/(tn + fp + fn + tp), (tp)/(fn + tp), (tp)/(fp + tp), (2*tp) / (2*tp + fp + fn)
    print('{} {}: Accuracy={} Recall={} Precision={} F-Measure={} logLoss={} '.format(test_name ,theWebsite, acc, recall, pre, fmeasure, logL))
 
def flat_train_test_df(dropFeatures = []):
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

    if dropFeatures != []:
        df = df.drop(dropFeatures, axis=1) 
        dft = dft.drop(dropFeatures, axis=1)

    return df, dft

group1 = ['id','tagclass','style', 'alt', 'align', 'itemprop', 'ariahidden', 'attrheight', 'attrwidth', 'lenattrs', 'LenHTML', 'parent1tag', 'parent2tag']
group2 = ['cached','fileext','lenimg', 'imgPosHTML', 'ratioimgpos', 'Width', 'Height', 'widthheight', 'rationwh', 'FileSize']
group3 = ['ratiotheimgPageimgs', 'ratiotheimgallimgs', 'orderfilesize', 'orderwidth', 'orderheight', 'orderwidthheight', 'cluster']

gain1 = ['cached', 'Width', 'widthheight', 'Height', 'FileSize']
gain2 = ['orderfilesize', 'ratiotheimgallimgs', 'orderwidth', 'ratiotheimgPageimgs', 'orderwidthheight']
gain3 = ['orderHeight', 'parent1tag', 'parent2tag', 'ratioimgpos', 'rationwh']
gain4 = ['fileext', 'attrheight', 'imgPosHTML', 'attrwidth', 'itemprop']
gain5 = ['cluster', 'lenimg', 'alt', 'lenattrs', 'LenHTML']

newfeatures =['cached', 'orderfilesize', 'ratiotheimgallimgs', 'orderwidth', 'ratiotheimgPageimgs', 'orderwidthheight', 'orderheight',
'ratioimgpos', 'attrheight', 'imgPosHTML', 'attrwidth', 'cluster', 'lenimg', 'lenattrs', 'LenHTML']
cachedFeat =['cached']

allfeats = group1 + group2 + group3
# test = list(set(allfeats) - set(group1) - set(group3) - set(group2))
# test = list(set(allfeats) - set(gain1) - set(gain2) - set(gain3) - set(gain4) - set(gain5))
# test = list(set(allfeats) - set(newfeatures))
test = cachedFeat

classification(test)




