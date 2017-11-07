#!/usr/bin/env python
# -*- coding: utf-8 -*-


author__ = 'Amit Mohapatra'

import json
import Pyro4
import hashlib
import logging as log

from common.reusable import Reusable
from semantic_algo.corpus_creator import CorpusCreator
from semantic_algo.semantic_similarity_algo import SemanticSimilarityAlgo


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class SemanticClassifier(object):

    def __init__(self, index_file_path):

        if Reusable.is_dir(index_file_path):
            self.index_file_path = index_file_path
        else:
            raise Exception("not a valid dir : %s" % index_file_path)
        self.semantic_min_score = 0.0
        self.service = SemanticSimilarityAlgo(self.index_file_path)
        self.corpus_obj = CorpusCreator(self)

    def __train_update(self, train_corpus):
        self.service.buffer(train_corpus)
        self.service.train(method=self.algo_name)
        self.service.index(train_corpus)

    def __validate_algoname(self, algo_name):

        if algo_name.lower() in ["lsi_tfidf", "lsi_logentropy", "lsi", "lda", "lda_logentropy", "lda_tfidf",
                                 "lda_multicore", "lda_multicore_tfidf", "lda_multicore_logentropy"]:
            self.algo_name = algo_name.lower()
        else:
            raise Exception("Algo name '%s' is not valid. It should be one of the among ['lsi_tfidf', "
                            "'lsi_logentropy', 'lsi', 'lda','lda_logentropy,, 'lda_tfidf', 'lda_mulricore']" % algo_name)

    def __validate_semantic_score(self, semantic_min_score):
        semantic_min_score = float(semantic_min_score)
        if (semantic_min_score >= 0.0) and (semantic_min_score <= 1.0):
            self.semantic_min_score = semantic_min_score
        else:
            raise Exception("semantic_min_score should be of range 0.0 to 1.0")

    def train(self, training_model, algo_name="lsi_logentropy"):
        """
        creting the model, then creating the index. test against the model.
        :param arg: tuple
        :return:
        """
        try:
            self.__validate_algoname(algo_name)
            train_corpus = self.corpus_obj.create_train_corpus(training_model)
            log.info("training model")
            self.__train_update(train_corpus)
            log.info("indexing finished")
        except:
            trace_err = Reusable.get_stack_trace()
            msg = "SemanticScoreGenerator (get_semantic_score()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    def predict(self, test_data, semantic_min_score=0.0):

        self.__validate_semantic_score(semantic_min_score)
        test_corpus = self.corpus_obj.create_test_corpus(test_data)
        final_result = []

        if test_corpus:

            for corpus in test_corpus:
                add_result = dict()
                semantic_result = []

                try:
                    semantic_result = self.service.find_similar(corpus, min_score=semantic_min_score)
                except Exception as e:
                    pass

                if semantic_result:
                    # sort the result.
                    sorted_result = self.__do_sort_result(semantic_result)
                    if sorted_result:
                        best_match = sorted_result[0]
                        last_underscore_index = best_match[0].rfind('_')
                        predicted_label = best_match[0][:last_underscore_index]
                        predicted_score = best_match[1]
                        add_result['predicted_label'] = predicted_label
                        add_result['predicted_score'] = predicted_score
                    else:
                        add_result["result"] = None
                else:
                    add_result["result"] = None
                final_result.append(add_result)
            self.corpus_obj.test_ids = []
            #Reusable.remove_multi_file_with_name(self.index_file_path+sep+"sqldict*")
            return json.dumps(final_result, ensure_ascii=False)
        else:
            add_result = dict()
            add_result["result"] = None
            final_result.append(add_result)

    def delete(self, ids_list):
        """
        delete the id from model and index.
        :param service: semantic similarity algo object
        :param id: indexed doc id
        :return: none
        """
        try:
            log.info("SemanticScoreGenerator : __delete_id() : started")
            self.service.delete(ids_list)
            log.info("SemanticScoreGenerator : __delete_id() : finished")
        except:
            trace_err = Reusable.get_stack_trace()
            msg = "SemanticScoreGenerator : __delete_id() : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    def __do_sort_result(self, semantic_result):
        """
        :param arg: tupple
        :return: sorted result
        sorting the result.
        """

        try:
            sorted_result = sorted([(r[0], r[1] * 100.0) for r in semantic_result], key=lambda t: t[1], reverse=True)
            print sorted_result
            return sorted_result
        except:
            trace_err = Reusable.get_stack_trace()
            msg = "SemanticScoreGenerator (__do_sort()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)


def main():

    Pyro4.Daemon.serveSimple(
        {
            SemanticClassifier("/Users/ricky/my_public_projects/index_store"): "example.semantic"
        },
        ns=False
    )

if __name__=="__main__":
    main()
