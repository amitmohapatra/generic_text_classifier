__author__ = 'ricky'

from os import path, sep

from textclassifier.semantic import SemanticTrainer

if __name__ == "__main__":

    base_path = path.dirname(path.dirname(__file__))
    model_store_path = "%s%s%s%s%s%s%s" % (base_path, sep, "resource", sep, "classifier_model", sep, "model1.json")

    s_obj = SemanticTrainer(algo_name='lsi_logentropy', semantic_min_score=0.75)
    s_obj.train(train_corpus)
    s_obj.fit(["jfjhf", "fjhfjf"])
    s_obj.predict()
    print s_obj.final_result
