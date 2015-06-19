import numpy as np
import matplotlib.pyplot as plt
import shared_scripts as ss
import sklearn.naive_bayes
from sklearn import cross_validation
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(cm, target_names, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def calculate_cv_confusion_matrix(y_true,y_pred,target_names,n_folds):
    
    cm_norm = np.zeros([len(target_names), len(target_names), n_folds])
    for i in range(n_folds):
        cm = confusion_matrix(y_true[i], y_pred[i])
        cm_norm[:,:,i] = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    np.set_printoptions(precision=2)

    print('Confusion matrix, with normalisation')
    print(np.mean(cm_norm,2))
    plt.figure()
    plot_confusion_matrix(np.mean(cm_norm,2),target_names)
    plt.show()

    print np.std(cm_norm,axis=2)
    plot_confusion_matrix(np.std(cm_norm,axis=2), target_names, title='Std of Confusion Matrix')
    plt.show()

if __name__ == "__main__":

    nyt = ss.load_data()
    clfNB = sklearn.naive_bayes.BernoulliNB()
    X, y, doc_term_matrix, feature_names = ss.train_data(nyt, clfNB)
    kfold = cross_validation.KFold(n=len(nyt.data),n_folds=3)
    y_pred, y_test, clf_score = ss.get_predictions(kfold, clfNB, doc_term_matrix, y)

    print clf_score
    print "The mean score is %1.2f" % np.mean(clf_score)
    calculate_cv_confusion_matrix(y_test,y_pred,nyt.target_names,kfold.n_folds)