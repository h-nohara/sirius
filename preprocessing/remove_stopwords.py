#!/usr/bin/env python
# -*- coding: utf-8 -*-

def remove_stopwords(doc, stopwords, replace=""):
    
    '''

    >>> sentence = "１１時と15じに３時のおやつ５0この123円、合計500円なり"
    >>> stopwords = ["時", "、"]
    >>> remove_stopwords(sentence, stopwords, "hoge")
    '１１hogeと15じに３hogeのおやつ５0この123円hoge合計500円なり'
    '''
    
    delete_for_str = str.maketrans(dict.fromkeys(stopwords, replace)) #第1引数: イテレータ, 第2引数: 置換後の文字列
    new_doc = doc.translate(delete_for_str)
    return new_doc

