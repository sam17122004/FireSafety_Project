import numpy as np
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix

def prf(y_true, y_pred, average="binary"):
    p,r,f,_ = precision_recall_fscore_support(y_true, y_pred, average=average, zero_division=0)
    return {"precision":p, "recall":r, "f1":f}

def confusion(y_true, y_pred, labels=None):
    return confusion_matrix(y_true, y_pred, labels=labels)
