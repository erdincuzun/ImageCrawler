import os
import pandas as pd
import numpy as np

from sklearn.metrics import log_loss

df = pd.read_csv('test_image_csv.csv', sep=',')

df['Prediction'] = np.where(df['orderfilesize'] == 1, 1, 0)

from sklearn.metrics import confusion_matrix
tn, fp, fn, tp = confusion_matrix(df['relevantImg'], df['Prediction']).ravel()
print(tn, fp, fn, tp)
print("Accuracy=", (tn+tp)/(tn + fp + fn + tp))
print("Recall=", (tp)/(fn + tp))
print("Precision=", (tp)/(fp + tp))
print("F-Measure= ", (2*tp / (2*tp + fp + fn)))
print("Log Loss= ", log_loss(df['relevantImg'], df['Prediction']))



