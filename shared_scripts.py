import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import cross_validation
from data_science_scripts import results_evaluation


def load_data():
    categories = ['Arts', 'Business', 'Obituaries', 'World', 'Sports']
    nyt = load_files("/Users/camcairns/Dropbox/Datasets/nyt_corpus/txt_document/", shuffle=True)
    return nyt


def train_data(nyt, clf):
    # Tokenize
    count_vect = CountVectorizer(decode_error='ignore')
    doc_term_matrix = count_vect.fit_transform(nyt.data)
    feature_names = np.array(count_vect.get_feature_names())
    X = np.array(nyt.data)
    y = np.array(nyt.target)
    return X, y, doc_term_matrix, feature_names


def get_predictions(kfold, clf, doc_term_matrix, y):
    y_pred = []
    y_test = []
    y_proba = []
    clf_score=[]
    for train, test in kfold:
        clf.fit(doc_term_matrix[train,:], y[train])
        clf_score.append(clf.score(doc_term_matrix[test,:], y[test]))
        y_pred.append(clf.fit(doc_term_matrix[train,:], y[train]).predict(doc_term_matrix[test,:]))
        y_test.append(y[test])
    return y_pred, y_test, clf_score

