__author__ = 'ricky'

from sklearn.datasets import fetch_20newsgroups
twenty_train = fetch_20newsgroups(subset='train', shuffle=True)
from sklearn.feature_extraction.text import TfidfTransformer

twenty_train.target_names #prints all the categories
#print("\n".join(twenty_train.data[0].split("\n")[:3])) #prints first line of the first data file

print len(twenty_train.data)
print(len(twenty_train.target))
twenty_test = fetch_20newsgroups(subset='test', shuffle=True)
print type(twenty_test.data)

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer(stop_words='english', min_df=3)
X_train_counts = count_vect.fit_transform(twenty_train.data)
X_train_counts.shape

from sklearn.feature_extraction.text import TfidfVectorizer
def tokens(x):
   return x.split(',')
tfidf_transformer = TfidfVectorizer(tokenizer=tokens ,use_idf=True, smooth_idf=True, sublinear_tf=False)
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

import numpy as np
twenty_test = fetch_20newsgroups(subset='test', shuffle=True)

vectors_test = tfidf_transformer.transform(twenty_test.data)

predicted = clf.predict(vectors_test)

print predicted
