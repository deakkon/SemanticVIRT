#imports
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

class ShevaClassificationMetrics:

    def computeClassificationMetrics(self, y_true,y_pred):
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        F1 = f1_score(y_true, y_pred)
        return (precision,recall, F1)