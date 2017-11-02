__author__ = 'ricky'

import json
from os import path, sep
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import BernoulliNB
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Algo used
bernoulli_pipeline = Pipeline([('vect', CountVectorizer(stop_words='english')),
                               ('tfidf', TfidfTransformer()),
                               ('clf', BernoulliNB()), ])

# tuning the algo
bernoulli_pipeline_param = {'vect__ngram_range': [(1, 2)],
                             'tfidf__use_idf': (True, False),
                             'tfidf__smooth_idf': (True, False),
                             'tfidf__sublinear_tf': (True, False),
                             'tfidf__norm': ('l1', 'l2'),
                             'clf__alpha': (1, 0.1, 0.01, 0.001, 0.0001), }

scores = ['precision', 'recall']

sgd_pipeline_param = {'vect__ngram_range': [(1, 2)],
                             'tfidf__use_idf': (True, False),
                             'tfidf__smooth_idf': (True, False),
                             'tfidf__sublinear_tf': (True, False),
                             'clf__alpha': (1, 0.1, 0.01, 0.001, 0.0001)}

sgd_pipeline = Pipeline([
                        ('vect', CountVectorizer(stop_words='english')),
                         ('tfidf', TfidfTransformer()),
                         ('clf', SGDClassifier(n_iter=50, penalty="elasticnet")),
                        ])

knn_pipeline_param = {'vect__ngram_range': [(1, 2)],
                             'tfidf__use_idf': (True, False),
                             'tfidf__smooth_idf': (True, False),
                             'tfidf__sublinear_tf': (True, False)}

knn_pipeline = Pipeline([
                        ('vect', CountVectorizer(stop_words='english')),
                         ('tfidf', TfidfTransformer()),
                         ('clf', KNeighborsClassifier(n_neighbors=10)),
                        ])

random_pipeline_param = {'vect__ngram_range': [(1, 2)],
                             'tfidf__use_idf': (True, False),
                             'tfidf__smooth_idf': (True, False),
                             'tfidf__sublinear_tf': (True, False)}

random_pipeline = Pipeline([
                        ('vect', CountVectorizer(stop_words='english')),
                         ('tfidf', TfidfTransformer()),
                         ('clf', RandomForestClassifier(n_estimators=100)),
                        ])

linear_pipeline_param = {'vect__ngram_range': [(1, 2)],
                             'tfidf__use_idf': (True, False),
                             'tfidf__smooth_idf': (True, False),
                             'tfidf__sublinear_tf': (True, False)}

linear_pipeline = Pipeline([
                        ('vect', CountVectorizer(stop_words='english')),
                         ('tfidf', TfidfTransformer()),
                         ('clf', LinearSVC(penalty='l2', dual=False,
                                       tol=1e-3)),
                        ])

des_pipeline_param = [{'vect__ngram_range': [(1, 2)],
                             'tfidf__use_idf': (True, False),
                             'tfidf__smooth_idf': (True, False),
                             'tfidf__sublinear_tf': (True, False)}]

des_pipeline = Pipeline([
                        ('vect', CountVectorizer(stop_words='english')),
                         ('tfidf', TfidfTransformer()),
                         ('clf', DecisionTreeClassifier(random_state=0)),
                        ])
# creating the pipeline to adopt any sklearn algo
#gs_clf = GridSearchCV(bernoulli_pipeline, bernoulli_pipeline_param, cv=5)
gs_clf = GridSearchCV(bernoulli_pipeline, bernoulli_pipeline_param, cv=5, error_score='precision')
# traing data and creating model

base_path = path.dirname(path.dirname(__file__))
model_store_path = "%s%s%s%s%s%s%s" % (base_path, sep, "resource", sep, "model", sep, "model.json")

train = []
label = []

data = {}
with open(model_store_path) as data_file:
    data = json.load(data_file)

for k, v in data.iteritems():
    len_v = len(v)
    train.extend(v)
    label.extend([k] * len_v)
print len(train)
model = gs_clf.fit(train, label)
result = model.predict(["jack daniel", "remmy martin", "roberto cavalli"])
print result
print model.best_estimator_
print model.scoring
#print accuracy_score(result, label, normalize=False)
#print accuracy_score(result, label)
