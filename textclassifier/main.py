#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ricky'

import json
import Pyro4

from semantic import SemanticClassifier

if __name__ == "__main__":

    index_file_path = "/Users/ricky/my_public_projects/index_store"
    model_store_path = "/Users/ricky/my_public_projects/full_model.json"

    train_corpus = {}
    with open(model_store_path) as data_file:
        train_corpus = json.load(data_file)

    l = []
    #train_corpus['beer'].extend(["soju is good for health and is very much fine", "nagaraja  iis a good and  so buy more",
    #                            "valadamir umeraja","valadamir umeraja chantamar best offer 100 ml", "valadamir umeraja  is  a good beer for 100 bucks"])

    from googletrans import Translator

    translator = Translator()



    s_obj =  Pyro4.Proxy("PYRO:example.semantic@localhost:65528")._pyroRelease()
    #s_obj.train(train_corpus, algo_name="lda_logentropy")
    print s_obj.predict("kingfisher beer")
    #s_obj.train_update([{"id": "whisky_1212", "tokens": ["soju 80ml"]}])
    print s_obj.predict(["kingfisher ber"])
    #s_obj.train_update([{"id": "whisky_1212", "tokens" : ["soju is nice "]}])
    print s_obj.predict(["magic moments"])
    s_obj.train({"beer":["soju is good for health and is very much fine", "nagaraja  iis a good and  so buy more",
                         "valadamir umeraja","valadamir umeraja chantamar best offer 100 ml", "valadamir umeraja  is  a good beer for 100 bucks"]})
    print s_obj.predict("soju is good for health very fine")
    print s_obj.predict("umeraja  is  a good  for ")
    print s_obj.predict("valadamir umeraja ")
    print s_obj.predict("nagaraja  iis a  ")

