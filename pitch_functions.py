from sklearn.metrics import f1_score, accuracy_score, roc_auc_score
from sklearn.preprocessing import LabelBinarizer

def calc_roc_acc_score(y_test, y_pred, average='macro'):
    """Calculate binary/multiclass AUC
       Returns: AUC
    """
    lb = LabelBinarizer()
    lb.fit(y_test)
    y_test = lb.transform(y_test)
    y_pred = lb.transform(y_pred)
    return roc_auc_score(y_test, y_pred, average=average)
   
def calc_acc_and_f1_score(true, preds, model_name='Model Name'):
    """Calc classification metrics and print them out
    """
    acc = accuracy_score(true, preds)
    f1 = f1_score(true, preds, average='weighted')
    multi_auc = calc_roc_acc_score(true, preds)
    #print('Model:{}'.format(model_name))
    print('Accuracy:{:.3f}'.format(acc))
    print('F1-Score: {:.3f}'.format(f1))
    print('AUC: {:.3f}'.format(multi_auc))