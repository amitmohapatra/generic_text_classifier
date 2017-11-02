__author__ = 'Amit Mohapatra'

import sys
import json
import shutil
import string
import traceback
import logging as log
from os import path, unlink, walk

from nltk import PorterStemmer, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

stop_words = stopwords.words('english')  # global declaration


class Reusable(object):
    """
    cleaning the file documents.
    """
    stemmer = PorterStemmer()

    def __init__(self, conf):
        self.conf = conf

    @staticmethod
    def get_stack_trace():
        """
        making the stack trace as string format.
        :return: stack trace as string
        """
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        trace_err = ''.join('!! ' + line for line in lines)
        return trace_err

    @staticmethod
    def empty_dir(dir_path):
        """
        cleaning a directory. removing files and directory inside it.
        :param dir_path: directory absolute path.
        :return: directory absolute path as string.
        """
        try:
            if Reusable.is_abs_path_exist(dir_path):
                pass

            for root, dirs, files in walk(dir_path):
                for f in files:
                    unlink(path.join(root, f))
                for d in dirs:
                    shutil.rmtree(path.join(root, d))

            return dir_path
        except:
            trace_err = Reusable.get_stack_trace()
            err_msg = "TextProcessor : empty_dir() : %s%s" % ("\n", trace_err)
            log.error(err_msg)
            raise Exception(err_msg)

    @staticmethod
    def stem_words(cleaned_words):
        try:
            final_stemming_content = [Reusable.stemmer.stem(word) for word in cleaned_words]
            return " ".join(final_stemming_content)
        except:
            trace_err = Reusable.get_stack_trace()
            msg = "TextProcessor (stem_words()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def is_abs_path_exist(my_path):
        """
        check if a path is absolute path or not
        :param my_path: path
        :return: boolean
        """

        if path.isabs(my_path):
            if path.exists(my_path):
                return True
            else:
                log.error("%s does not exist" % my_path)
                raise Exception("%s does not exist" % my_path)
        else:
            log.error("%s is not absolute" % my_path)
            raise Exception("%s is not absolute" % my_path)

    @staticmethod
    def is_dir(my_path):
        """
        check if a path is absolute path or not
        :param my_path: path
        :return: boolean
        """

        if path.isdir(my_path):
            if path.exists(my_path):
                return True
            else:
                log.error("dir %s does not exist" % my_path)
                raise Exception("dir %s does not exist" % my_path)
        else:
            log.error("%s is not a directory" % my_path)
            raise Exception("%s is not a director" % my_path)

    @staticmethod
    def read_file(file_path):
        """
        reading a file.
        :param file_path: absolute file path
        :return: file content as string
        """
        try:
            file_content = None
            try:
                myfile = open(file_path, "r")
                try:
                    file_content = myfile.read()
                finally:
                    myfile.close()
            except Exception as e:
                raise
            return file_content
        except:
            trace_err = Reusable.get_stack_trace()
            msg = "TextProcessor (read_file()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def load_json_from_file(file_path):
        """
        reading a file.
        :param file_path: absolute file path
        :return: file content as string
        """
        try:
            data = None
            try:
                with open(file_path) as data_file:
                    data = json.load(data_file)
            except Exception as e:
                raise
            return data
        except:
            trace_err = Reusable.get_stack_trace()
            msg = "TextProcessor (read_file()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def load_json_from_string(json_string):
        """
        reading a file.
        :param file_path: absolute file path
        :return: file content as string
        """
        try:
            data = None
            try:
                data = json.load(json_string)
            except Exception as e:
                raise
            return data
        except:
            trace_err = Reusable.get_stack_trace()
            msg = "TextProcessor (read_file()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def sentence_tokenize(text):
        """
        nltk module has been used to tokenize sentence and then make it to word tokenize.
        :param text: processed file content
        :return: tokenize words as list.
        """
        try:
            if text:
                sent_tokenize_list = sent_tokenize(text)
                res = []

                for sent in sent_tokenize_list:
                    word_tokens = word_tokenize(sent)
                    tokens = []

                    for word in word_tokens:
                        word = word.strip('`~!@#$%^&*()_+-={}|[]:";<>?,.').strip('`~!@#$%^&*()_+-={}|[]:";<>?,.')\
                               .strip('`~!@#$%^&*()_+-={}|[]:";<>?,.')
                        tokens.append(word)

                    tokens = [i for i in tokens if i not in string.punctuation]
                    tokens = [i for i in tokens if i not in stop_words]
                    res.extend(tokens)
                return res
            else:
                return []
        except:
            trace_err = Reusable.get_stack_trace()
            msg = "TextProcessor (sentence_tokenize()) : error while tokenizing sentence : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def strip_text(text):
        """
        strip \n, \t, \r and replace with a space.
        :param text: file content.
        :return: processed file content.
        """
        try:
            if text:
                return str(text).replace("\n", " ").replace("\t", " ").replace("\r", " ").strip().lower()
            else:
                return " "
        except:
            trace_err = Reusable.get_stack_trace()
            msg = "TextProcessor (strip_text()) : error while striping sentence : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def remove_codec(text):
        """
        text codec can be any format. making all codec to printable text.
        removing machine unredable characters.
        :param text: file content
        :return: processed file content.
        """
        try:
            if text:
                if not isinstance(text, (int, long)):
                    text = filter(lambda x: x in string.printable, text)
                return Reusable.strip_text(text)
            else:
                return " "
        except:
            trace_err = Reusable.get_stack_trace()
            msg = "TextProcessor (remove_codec()) : error while removing codec : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)
