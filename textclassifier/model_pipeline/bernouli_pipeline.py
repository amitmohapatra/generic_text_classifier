__author__ = 'ricky'


from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.grid_search import GridSearchCV
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from textclassifier.text_processor.text_normalizer import TextNormalizer
from textclassifier.text_processor.text_stats import TextStats

from sklearn.naive_bayes import BernoulliNB

def construct_pipeline(estimator, **kwargs):
    return Pipeline([
        # Create a Feature Union of Text Stats and Bag of Words
        ('features', FeatureUnion(
            transformer_list=[

                # Pipeline for pulling document structure features
                ('stats', Pipeline([
                    ('stats', TextStats()),
                    ('vect', DictVectorizer()),
                ])),

                # Pipeline for creating a bag of words TF-IDF vector
                ('bow', Pipeline([
                    ('tokens', TextNormalizer()),
                    ('tfidf',  TfidfVectorizer()),
                    ('best', TruncatedSVD(n_components=10000)),
                ])),

            ],

            # weight components in feature union
            transformer_weights={
                'stats': 0.15,
                'bow': 0.85,
            },
        )),

        # Append the estimator to the end of the pipeline
        ('model', estimator(**kwargs)),
    ])
"""
bernoulli_pipeline = Pipeline([('vect', DictVectorizer()),
                               ('tfidf', TfidfVectorizer()),
                               ('clf', BernoulliNB()),
                               ('stats', TextStats()),
                               ('best', TruncatedSVD(n_components=10000)),
                            ])
"""
bernoulli_pipeline = Pipeline([('vect', CountVectorizer(stop_words='english')),
                               ('tfidf', TfidfVectorizer()),
                               ('clf', BernoulliNB()), ])

bernoulli_pipeline_param = {'vect__ngram_range': [(1, 2)],
                             'tfidf__use_idf': (True, False),
                             'tfidf__smooth_idf': (True, False),
                             'tfidf__sublinear_tf': (True, False),
                             'tfidf__norm': ('l1', 'l2'),
                             'clf__alpha': (1, 0.1, 0.01, 0.001, 0.0001), }

gs_clf = GridSearchCV(bernoulli_pipeline, bernoulli_pipeline_param, cv=5)
# traing data and creating model

model_store_path = "/Users/ricky/my_public_projects/full_model.json"

train = []
label = []

import json
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