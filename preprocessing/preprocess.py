#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, sys, glob2
import numpy as np
import pandas as pd
from pandas import DataFrame, Series

from .remove_stopwords import remove_stopwords
from .stopwords_config import stop_words_1, stop_words_2
from .split_by_sentence import split_by_sentence
from .normalize_number import normalize_number, normalize_number_specified_pattern
from .mecab_handlers import doc_to_words


def load_docs(csv_path, cols=None):
    
    df = pd.read_csv(csv_path, index_col=0)

    if cols is None:
        return df
    else:
        docs = {col: list(df.loc[:, col]) for col in cols}
        return docs


class Preprocessing:
    
    '''
    各文書の単語リストを作成

    ** 文書単位の場合

    >>> prepro = Preprocessing(docs)
    >>> prepro.check_nan_doc()  # np.nanの文章をチェック
    >>> prepro.to_unique()  # ユニークな文章だけにする
    >>> prepro.normalize_number()  # 数字を正規化
    >>> prepro.remove_stopwords(stop_words=stop_words_1, replace="")  # stopワードを削除
    >>> prepro.wakati(parts=["名詞"])  # 分かち書きして名詞のみを使う
    >>> words_list = prepro.words_list

    ** 文単位の場合

    >>> prepro = Preprocessing(docs)
    >>> prepro.check_nan_doc()  # np.nanの文章をチェック
    >>> prepro.normalize_number()  # 数字を正規化
    >>> prepro.split_by_sentence(stop_words=stop_words_2)  # stopワードをの部分で文単位に分割
    >>> prepro.remove_stopwords_by_sentence(stop_words=stop_words_1)  # stopワードを削除
    >>> prepro.to_unique_by_sentence()  # ユニークな文章のみにする
    >>> prepro.wakati_by_sentence(parts=["名詞"])  # 分かち書きして名詞のみを使う
    >>> words_list = prepro.words_list

    '''

    def __init__(self, docs):

        self.docs = docs
        self.docs_per_sentence = []  # 文単位用
        self.words_list = []
        self.words_list_by_sentence = []  # 文単位用

    
    def check_nan_doc(self):

        '''
        元の文章をpandas.DaraFrameを使って読み込んでいるので、np.nanになっている文章があれば" "にする
        '''
        
        for i, doc in enumerate(self.docs):
            if doc is np.nan:
                self.docs[i] = " "


    def normalize_number(self, patterns=None, replace="0"):
        
        '''
        数字の連続を指定の文字に統一する
        '''
        
        if patterns is None:
            for i, doc in enumerate(self.docs):
                self.docs[i] = normalize_number(doc, replace)
        
        else:
            for i, doc in enumerate(self.docs):
                self.docs[i] = normalize_number_specified_pattern(doc, patterns, replace)


    def split_by_sentence(self, stopwords):
        
        '''
        文単位で分割
        '''

        for doc in self.docs:
            sentences = split_by_sentence(doc, stopwords)
            self.docs_per_sentence.append(sentences)


    
    def remove_stopwords(self, stop_words=stop_words_1, replace=""):
        
        '''
        指定した文字を削除
        '''
        
        for i, doc in enumerate(self.docs):
            self.docs[i] = remove_stopwords(doc, stop_words, replace)

    
    def remove_stopwords_by_sentence(self, stop_words=stop_words_1, replace=""):
        
        '''
        指定した文字を削除（文単位用）
        '''

        for i, sentences in enumerate(self.docs_per_sentence):
            for j, sentence in enumerate(sentences):
                self.docs_per_sentence[i][j] = remove_stopwords(sentence, stop_words, replace)


    def to_unique(self):
        
        '''
        ユニークな文章のみにする
        '''

        n_doc = len(self.docs)
        unique_docs = list(dict.fromkeys(self.docs))
        n_unique_doc = len(unique_docs)
        print("uniformed : {} docs -> {} docs".format(n_doc, n_unique_doc))
        self.docs = unique_docs


    def to_unique_by_sentence(self):
        
        '''
        ユニークな文章のみにする（文単位用）
        '''

        seen = []
        unique_docs = []

        for sentences in self.docs_per_sentence:
            sentences_this_doc = []
            for sentence in sentences:
                if sentence not in seen:
                    sentences_this_doc.append(sentence)
                    seen.append(sentence)
            unique_docs.append(sentences_this_doc)

        assert len(self.docs) == len(unique_docs)

        n_sentence = 0
        for l in self.docs_per_sentence:
            n_sentence += len(l)

        n_unique_sentence = 0
        for l in unique_docs:
            n_unique_sentence += len(l)

        print("uniformed : {} docs -> {} docs".format(n_sentence, n_unique_sentence))

        self.docs_per_sentence = unique_docs

            


    def wakati(self, parts=None):
        
        '''
        分かち書き
        '''
        
        for doc in self.docs:
            words = doc_to_words(doc, parts)
            self.words_list.append(words)

        assert len(self.words_list) == len(self.docs)


    def wakati_by_sentence(self, parts=None):
        
        '''
        分かち書き（文単位用）
        '''
        
        for sentences in self.docs_per_sentence:
            words_this_doc = []
            for sentence in sentences:
                words = doc_to_words(sentence, parts)
                words_this_doc.append(words)
            self.words_list_by_sentence.append(words_this_doc)

        assert len(self.words_list_by_sentence) == len(self.docs)
