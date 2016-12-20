import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_files
import sklearn.naive_bayes
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import cross_validation
from data_science_scripts import results_evaluation


def highest_coefficents(N, feature_names):
    for target_class in range(5):
        idx = np.argsort(clfNB.feature_log_prob_[target_class])
        print "The most likely %d words to appear in a document of class %s are:" % (N, categories[target_class])
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
    for target_class in range(5):
        discrimination_metric, discrimination_metric_signed = calc_discrimination_metric(target_class, nyt, clfNB)
        idx = np.argsort(discrimination_metric)
        print "The most discrminating %d words for class %s are:" % (N, categories[target_class])
        print feature_names[idx][::-1][:N]
        print "They have probabilities:"
        print discrimination_metric_signed[idx][::-1][:N]

if __name__ == "__main__":
    categories = ['Arts', 'Business', 'Obituaries', 'World', 'Sports']
    nyt = load_files("/Users/camcairns/Dropbox/Datasets/nyt_corpus/txt_document/", shuffle=True)
    kfold = cross_validation.KFold(n=len(nyt.data), n_folds=3)
    clfNB = sklearn.naive_bayes.BernoulliNB()
    # Tokenize
    count_vect = CountVectorizer(decode_error='ignore', ngram_range=(1, 4))
    doc_term_matrix = count_vect.fit_transform(nyt.data)
    feature_names = np.array(count_vect.get_feature_names())
    X = np.array(nyt.data)
    y = np.array(nyt.target)
    y_pred = []
    y_test = []
    y_proba = []
    mispredicted_proba = []

    for train, test in kfold:
        X[train]
        y[train]
        clfNB.fit(doc_term_matrix[train, :], y[train])
        y_pred.append(clfNB.fit(doc_term_matrix[train, :], y[train]).predict(doc_term_matrix[test, :]))
        y_test.append(y[test])

    most_discriminating_words(10, feature_names)
    results_evaluation.calculate_cv_confusion_matrix(y_test, y_pred, nyt.target_names, kfold.n_folds)


