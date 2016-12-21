import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.datasets import load_files
import sklearn.naive_bayes
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import cross_validation
from sklearn.metrics import confusion_matrix
# from data_science_scripts import results_evaluation


def highest_coefficents(N, feature_names):
    for i, category in enumerate(nyt.target_names):
        idx = np.argsort(clfNB.feature_log_prob_[i])
        print "The most likely {0} words to appear in a document of class {1} are:".format(N, category)
        print 'Probabilities', np.exp(clfNB.feature_log_prob_[2][idx][::-1][:10])
        feature_names[idx][::-1][:10]


def calc_discrimination_metric(target_class, dataset, classifier):
    ckd_range = range(len(dataset.target_names))
    ckd_range.remove(target_class)
    feature_prob_ = np.exp(classifier.feature_log_prob_)
    discrimination_metric = sum(np.abs(feature_prob_[target_class, :] - feature_prob_[ckd_range, :]), 0)
    discrimination_metric = discrimination_metric/len(ckd_range)
    discrimination_metric_signed = sum(feature_prob_[target_class, :] - feature_prob_[ckd_range, :], 0)
    discrimination_metric_signed = discrimination_metric_signed/len(ckd_range)
    return discrimination_metric, discrimination_metric_signed


def most_discriminating_words(N, feature_names):


def calculate_cv_confusion_matrix(y_true, y_pred, target_names, n_folds):
    cm_norm = np.zeros([len(target_names), len(target_names), n_folds])
    for i in range(n_folds):
        cm = confusion_matrix(y_true[i], y_pred[i])
        cm_norm[:, :, i] = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    np.set_printoptions(precision=2)

    print('Confusion matrix, with normalisation')
    print(np.mean(cm_norm, 2))
    plt.figure()
    plot_confusion_matrix(np.mean(cm_norm, 2), target_names)

    print np.std(cm_norm, axis=2)
    plot_confusion_matrix(np.std(cm_norm, axis=2), target_names, title='Std of Confusion Matrix')


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
    plt.tight_layout()
    plt.savefig('./results/' + title.lower().replace(" ", "_") + ".png", transparant=True)
    plt.close()

def get_predictions(kfold, clf, doc_term_matrix, y):
    y_pred = []
    y_test = []
    y_proba = []
    clf_score=[]
    for train, test in kfold:
        clf.fit(doc_term_matrix[train,:], y[train])
        clf_score.append(clf.score(doc_term_matrix[test, :], y[test]))
        y_pred.append(clf.fit(doc_term_matrix[train, :], y[train]).predict(doc_term_matrix[test,:]))
        y_test.append(y[test])
    return y_pred, y_test, clf_score

if __name__ == "__main__":
    nyt = load_files(os.environ["data_dir"] + "/nyt_corpus/txt_document/", shuffle=True)
    kfold = cross_validation.KFold(n=len(nyt.data), n_folds=3)
    clfNB = sklearn.naive_bayes.BernoulliNB()
    # Tokenize
    count_vect = CountVectorizer(decode_error='ignore', ngram_range=(1, 1))
    doc_term_matrix = count_vect.fit_transform(nyt.data)
    feature_names = np.array(count_vect.get_feature_names())
    X = np.array(nyt.data)
    y = np.array(nyt.target)
    y_pred = []
    y_test = []
    y_proba = []
    mispredicted_proba = []

    # predict hold-out set and plot confusion matrix
    y_pred, y_test, clf_score = get_predictions(kfold, clfNB, doc_term_matrix, y)
    print clf_score
    print "The mean score is %1.2f" % np.mean(clf_score)
    calculate_cv_confusion_matrix(y_test, y_pred, nyt.target_names, kfold.n_folds)

    # get most discriminating ngrams for each category
    most_discriminating_words(10, feature_names)

