import numpy as np
import shared_scripts as ss

def highest_coefficents(N, feature_names):
    for target_class in range(5):
        idx = np.argsort(clfNB.feature_log_prob_[target_class])
        print "The most likely %d words to appear in a document of class %s are:" % (N, categories[target_class])
        print 'Probabilities', np.exp(clfNB.feature_log_prob_[2][idx][::-1][:10])
        feature_names[idx][::-1][:10]

def calc_discrimination_metric(target_class, dataset, classifier):
    ckd_range = range(len(dataset.target_names))
    ckd_range.remove(target_class) # complement kronecker delta: 1-delta
    feature_prob_ = np.exp(classifier.feature_log_prob_)
    discrimination_metric = sum(np.abs(feature_prob_[target_class,:] - feature_prob_[ckd_range,:]),0)
    discrimination_metric = discrimination_metric/len(ckd_range)
    discrimination_metric_signed = sum(feature_prob_[target_class,:] - feature_prob_[ckd_range,:],0)
    discrimination_metric_signed = discrimination_metric_signed/len(ckd_range)
    return discrimination_metric, discrimination_metric_signed

def most_discriminating_words(N, feature_names):
    for target_class in range(5):
        discrimination_metric, discrimination_metric_signed = calc_discrimination_metric(target_class,nyt,clfNB)
        idx = np.argsort(discrimination_metric)
        print "The most discrminating %d words for class %s are:" % (N, categories[target_class])
        print feature_names[idx][::-1][:N]
        print "They have probabilities:"
        print discrimination_metric_signed[idx][::-1][:N]

if __name__ == "__main__":

nyt = ss.load_data()
X, y, doc_term_matrix, feature_names = train_data(nyt)

kfold = cross_validation.KFold(n=len(nyt.data),n_folds=3)
y_pred, y_test = get_predictions(kfold)

most_discriminating_words(10, feature_names)