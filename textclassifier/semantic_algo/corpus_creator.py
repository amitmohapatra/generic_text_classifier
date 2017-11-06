__author__ = 'ricky'

import hashlib
from os import sep
import logging as log
from gensim import utils
from common.reusable import Reusable


class CorpusCreator(object):

    def __init__(self, semantic_obj):
        self.semantic_obj = semantic_obj
        self.corpus_dir_path = Reusable.create_dir("%s%s%s" % (self.semantic_obj.index_file_path, sep, "train_corpus"))
        self.corpus_file_path = "%s%s%s" % (self.corpus_dir_path, sep, "train.pkl")

    def __read_write_train_to_disk(self, new_train):

        if Reusable.is_abs_path_exist(self.corpus_file_path):
            old_train = Reusable.read_pickle_file(self.corpus_file_path)
            new_train.update(old_train)
        log.info("writing traing model for future use")
        Reusable.write_pickle_file(self.corpus_file_path, new_train)
        log.info("writing traing model finished")
        return [{"id": k, "tokens": v} for k, v in new_train.items()]

    def create_train_corpus(self, traing_model):

        try:
            train_corpus = {}
            for model_label, model_value_list in traing_model.items():
                count = 0

                if isinstance(model_value_list, basestring):
                    model_value_list = [model_value_list]

                for each_val in model_value_list:
                    token_value = self.__clean_text(each_val)

                    if token_value:
                        id_ = int(hashlib.md5(repr(each_val).decode('utf-8')).hexdigest(), 16)
                        train_corpus["%s_%s" % (model_label, id_)] = token_value
                    else:
                        log.warning("model label %s and vale %s failed" % (model_label, each_val))
                    count += 1
            return self.__read_write_train_to_disk(train_corpus)
        except Exception:
            trace_err = Reusable.get_stack_trace()
            msg = "CorpusCreator (create_train_corpus) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise

    def create_test_corpus(self, test_data):

        try:
            test_corpus = []
            count = 0

            if isinstance(test_data, basestring):
                test_data = [test_data]

            for each_val in test_data:
                token_value = self.__clean_text(each_val)
                if token_value:
                    corpus_format = {"tokens": token_value}
                    test_corpus.append(corpus_format)
                else:
                    add_result = dict()
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
