import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_files
import sklearn.naive_bayes
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import cross_validation
from data_science_scripts import results_evaluation


categories = ['Arts','Business','Obituaries','World','Sports']
nyt = load_files("/Users/camcairns/Dropbox/Datasets/nyt_sections/txt_document/", shuffle=True)

kfold = cross_validation.KFold(n=len(nyt.data),n_folds=3)
clfNB = sklearn.naive_bayes.MultinomialNB()

# Tokenize
count_vect = CountVectorizer(decode_error='ignore')
doc_term_matrix = count_vect.fit_transform(nyt.data)

X = np.array(nyt.data)
y = np.array(nyt.target)
y_pred = []
y_test = []
for train, test in kfold:
    X[train]
    y[train]
    clfNB.fit(doc_term_matrix[train,:], y[train])
    y_pred.append(clfNB.fit(doc_term_matrix[train,:], y[train]).predict(doc_term_matrix[test,:]))
    y_test.append(y[test])
    
results_evaluation.calculate_cv_confusion_matrix(y_test,y_pred,nyt.target_names,kfold.n_folds)