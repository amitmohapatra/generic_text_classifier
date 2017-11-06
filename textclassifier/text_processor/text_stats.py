__author__ = 'ricky'


from collections import Counter
from sklearn.base import BaseEstimator, TransformerMixin


class TextStats(BaseEstimator, TransformerMixin):

    def fit(self, documents, labels=None):
        vocabulary = Counter(
            token for paragraph in documents
            for sentence in paragraph
            for token, tag in sentence
        )

        self.corpus_vocab = len(vocabulary)
        self.corpus_count = sum(vocabulary.items())
        return self

    def transform(self, documents):
        for document in documents:
            # Collect token and vocabulary counts
            counts = Counter(
                item[0] for para in document for sent in para for item in sent
            )

            # Yield structured information about the document
            yield {
                'paragraphs': len(document),
                'sentences': sum(len(para) for para in document),
                'words': sum(counts.values()),
                'vocab': len(counts),
            }
