__author__ = 'ricky'

from sklearn.naive_bayes import BernoulliNB

"""
def build_model(corpus, estimator, **kwargs):

    # Create a loader for scoring.
    loader = CorpusLoader(corpus, 12)
    scores = []

    # Perform 12-part cross validation
    for fold in range(12):
        # Get the train data sets
        docs_train = loader.documents(fold, train=True)
        labels_train = loader.labels(fold, train=True)

        # Create and fit the model
        model = create_pipeline(estimator, **kwargs)
        model.fit(docs_train, labels_train)

        # Get the score of the model on the test data
        docs_test = loader.documents(fold, test=True)
        labels_test = loader.labels(fold, test=True)
        scores.append(model.score(docs_test, labels_test))

    # Build the final model on the entire dataset
    loader = CorpusLoader(corpus, None)
    model = create_pipeline(estimator, **kwargs)
    model.fit(loader.documents(), loader.labels())

    return model, scores
"""


class BernouliClassifier:

    def __init__(self):
        pass

    def train(self):
        pass

    def predict(self):
        pass

    def update(self):
        pass
