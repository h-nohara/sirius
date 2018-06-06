#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, glob2
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from collections import defaultdict
from gensim import corpora, models, similarities, matutils

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from .mecab_handlers import doc_to_words
from Word2Vec import W2V_model



def make_dictionary(words_list, save_path=None):
    
    dictionary = corpora.Dictionary(words_list)
    if save_path:
        dictionary.save_as_text(save_path)
    return dictionary


def load_dictionary(dict_path):
    
    dictionary = corpora.Dictionary.load_from_text(dict_path)
    return dictionary


def update_dictionary(dictionary, words_list, save_path=None):
    
    dictionary.add_documents(words_list)
    if save_path:
        dictionary.save_as_text(save_path)
    return dictionary


def make_one_corpus(dictionary, words):
    
    one_corpus = dictionary.doc2bow(words)
    return one_corpus


def make_corpus(dictionary, words_list):
    
    corpus = [make_one_corpus(dictionary, words) for words in words_list]
    return corpus



def corpus_to_arr(dictionary, corpus):
    
    '''
    :return: インデックスがid, 値がカウント数のシリーズ
    '''
    
    ids = sorted(dictionary.keys())
    s = Series(np.zeros(len(ids)), index=ids)

    for tup in corpus:
        dict_id = tup[0]
        count = tup[1]
        s[dict_id] = count

    return s
