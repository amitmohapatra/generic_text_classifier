#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ricky'

import json

from semantic import SemanticClassifier

if __name__ == "__main__":

    index_file_path = "/Users/ricky/my_public_projects/index_store"
    model_store_path = "/Users/ricky/my_public_projects/full_model.json"

    train_corpus = {}
    with open(model_store_path) as data_file:
        train_corpus = json.load(data_file)

    l = []
    train_corpus['beer'].append(u"史密斯是王明的朋友")


    from googletrans import Translator

    translator = Translator()


    s_obj = SemanticClassifier(index_file_path, algo_name='lda_logentropy', semantic_min_score=0.8)
    #s_obj.train(train_corpus)

    s_obj.predict([u"史密斯是王明的朋友"])
    print json.dumps(s_obj.final_result, ensure_ascii=False)


