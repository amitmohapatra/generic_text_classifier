__author__ = 'ricky'

import logging as log
from gensim import utils
from common.reusable import Reusable


class CorpusCreator(object):

    def __init__(self, traing_model):
        self.traing_model = traing_model
        self.train_corpus = []
        self.test_corpus = []
        self.test_ids = []
        self.actual_match_with = dict()

    def create_train_corpus(self):

        try:
            for model_label, model_value_list in self.traing_model.iteritems():
                count = 0
                for each_val in model_value_list:
                    token_value = self.__clean_text(each_val)
                    if token_value:
                        self.actual_match_with["%s_*&$*_%s" % (model_label, count)] = each_val
                        corpus_format = {"id": "%s_*&$*_%s" % (model_label, count), "tokens": token_value}
                        self.train_corpus.append(corpus_format)
                    else:
                        log.warning("model label %s and vale %s failed" % (model_label, each_val))
                    count += 1
        except:
            trace_err = Reusable.get_stack_trace()
            msg = "CorpusCreator (create_corpus) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    def create_test_corpus(self, test_data):
        count = 0
        for each_val in test_data:
            token_value = self.__clean_text(each_val)
            if token_value:
                self.test_ids.append(["_*&$*_%s" % count, each_val])
                corpus_format = {"id": "__%s" % count, "tokens": token_value}
                self.test_corpus.append(corpus_format)
            else:
                log.warning("model label %s and vale %s failed" % ("__%s" % count, each_val))
            count += 1

    def __clean_text(self, each_val):
        cleaned_doc_tokens = Reusable.sentence_tokenize(Reusable.remove_codec(each_val))
        stem_doc = Reusable.stem_words(cleaned_doc_tokens)
        token_value = utils.simple_preprocess(stem_doc)
        return token_value
