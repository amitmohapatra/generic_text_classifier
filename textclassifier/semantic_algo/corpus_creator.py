__author__ = 'ricky'

import hashlib
import logging as log
from gensim import utils
from common.reusable import Reusable


class CorpusCreator(object):

    def __init__(self, semantic_obj):
        self.test_ids = []
        self.actual_match_with = dict()
        self.semantic_obj = semantic_obj

    def create_train_corpus(self, traing_model):

        try:
            train_corpus = []
            for model_label, model_value_list in traing_model.items():
                count = 0
                for each_val in model_value_list:
                    token_value = self.__clean_text(each_val)
                    if token_value:
                        id_ = int(hashlib.md5(repr(each_val).decode('utf-8')).hexdigest(), 16)
                        corpus_format = {"id": "%s_%s" % (model_label, id_), "tokens": token_value}
                        train_corpus.append(corpus_format)
                    else:
                        log.warning("model label %s and vale %s failed" % (model_label, each_val))
                    count += 1
            return train_corpus
        except Exception:
            trace_err = Reusable.get_stack_trace()
            msg = "CorpusCreator (create_train_corpus) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise

    def create_test_corpus(self, test_data):

        try:
            test_corpus = []
            count = 0
            for each_val in test_data:
                token_value = self.__clean_text(each_val)
                if token_value:
                    id_ = int(hashlib.md5(repr(each_val).decode('utf-8')).hexdigest(), 16)
                    self.test_ids.append(["%s" % id_, each_val])
                    corpus_format = {"id": "%s" % id_, "tokens": token_value}
                    test_corpus.append(corpus_format)
                else:
                    add_result = dict()
                    add_result["query"] = each_val
                    add_result["result"] = None
                    self.semantic_obj.final_result.append(add_result)
                    log.warning("query '%s' dint process bcoz it is not a valid document" % each_val)
                count += 1
            return test_corpus
        except Exception:
            trace_err = Reusable.get_stack_trace()
            msg = "CorpusCreator (create_test_corpus) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise

    def __clean_text(self, each_val):
        cleaned_doc_tokens = Reusable.sentence_tokenize(each_val)
        stem_doc = Reusable.stem_words(cleaned_doc_tokens)
        token_value = utils.simple_preprocess(stem_doc)
        return token_value
