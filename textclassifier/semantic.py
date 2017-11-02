__author__ = 'Amit Mohapatra'

import logging as log
from common.reusable import Reusable
from semantic_algo.corpus_creator import CorpusCreator
from semantic_algo.semantic_similarity_algo import SemanticSimilarityAlgo


class SemanticClassifier(object):

    def __init__(self, index_file_path, algo_name="lsi_logentropy", semantic_min_score=0.0):
        self.service = None


        if Reusable.is_dir(index_file_path):
            self.index_file_path = index_file_path
        else:
            raise Exception("not a valid dir : %s" % index_file_path)

        self.algo_name_exist = algo_name.lower() in ["lsi_tfidf", "lsi_logentropy", "lsi", "lda",
                                                     "lda_logentropy", "lda_tfidf"]
        if self.algo_name_exist:
            self.algo_name = algo_name.lower()
        else:
            raise Exception("Algo name '%s' is not valid. It should be one of the among ['lsi_tfidf', "
                            "'lsi_logentropy', 'lsi', 'lda','lda_logentropy,, 'lda_tfidf']" % algo_name)

        semantic_min_score = float(semantic_min_score)
        if (semantic_min_score >= 0.0) and (semantic_min_score <= 1.0):
            self.semantic_min_score = semantic_min_score
        else:
            raise Exception("semantic_min_score should be of range 0.0 to 1.0")

        self.final_result = []
        self.corpus_obj = CorpusCreator()

    def train(self, training_model):
        """
        creting the model, then creating the index. test against the model.
        :param arg: tuple
        :return:
        """
        try:
            self.corpus_obj.create_train_corpus(training_model)
            log.info("training model")
            self.service = SemanticSimilarityAlgo(self.index_file_path)
            self.service.train(corpus_obj.train_corpus, method=self.algo_name)
            self.service.index(corpus_obj.train_corpus)
            self.service.optimize()
            log.info("indexing finished")
        except:
            trace_err = Reusable.get_stack_trace()
            msg = "SemanticScoreGenerator (get_semantic_score()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    def predict(self, test_data):

        test_corpus = self.corpus_obj.create_test_corpus(test_data)
        self.service.index(test_corpus)

        for label_data in self.corpus_obj.test_ids:
            label_id = label_data[0]
            label_text = label_data[1]
            semantic_result = self.service.find_similar(label_id, min_score=self.semantic_min_score)
            add_result = dict()
            add_result["query"] = label_text

            if semantic_result:
                # sort the result.
                sorted_result = self.__do_sort_result(label_id, semantic_result)
                best_match = sorted_result[0]
                prdict_label = best_match[0].split("_*&$*_")[0]
                prdict_score = best_match[1]
                add_result['predicted_label'] = prdict_label
                add_result['predicted_score'] = prdict_score
                add_result['matched_doc'] = self.corpus_obj.actual_match_with[best_match[0]]
            else:
                add_result["result"] = None
            self.final_result.append(add_result)

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

    def __do_sort_result(self, id, semantic_result):
        """
        :param arg: tupple
        :return: sorted result
        sorting the result.
        """

        try:
            sorted_result = sorted([(r[0], r[1] * 100.0) for r in semantic_result
                                    if str(r[0]) != str(id)], key=lambda t: t[1], reverse=True)
            return sorted_result
        except:
            trace_err = Reusable.get_stack_trace()
            msg = "SemanticScoreGenerator (__do_sort()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)