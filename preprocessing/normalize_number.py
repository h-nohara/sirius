#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def normalize_number(doc, replace="0"):
    
    '''
    連続した数字を0で置換

    >>> sentence = "江頭2:50は40度の高熱でも元気である。ギャラも500円でも気にしない。"
    >>> normalize_number(sentence, "12")
    '江頭12:12は12度の高熱でも元気である。ギャラも12円でも気にしない。'
    '''

    replaced_doc = re.sub("\d+", replace, doc)
    return replaced_doc



def  normalize_number_specified_pattern(doc, patterns={"prefix":[], "suffix":[]}, replace="0"):
    
    '''
    特定のパターンで出てきた数字を置き換える

    >>> sentence = "１１時15じに３時のおやつ５0この123円槌合計500なり"
    >>> normalize_number_specified_pattern(sentence, {"prefix":["合計"], "suffix":["時", "円", "こ"]}, replace_word="0")
    '0時15じに0時のおやつ0この0円槌合計0なり'
    '''
    
    pref_patterns = [("{}+\d+".format(pref), pref) for pref in patterns["prefix"]]    
    suff_patterns = [("\d+{}".format(suff), suff) for suff in patterns["suffix"]]
    
    for pattern, pref in pref_patterns:
        if re.findall(pattern, doc):
            doc = re.sub(pattern, pref+replace, doc)
    
    for pattern, suff in suff_patterns:
        if re.findall(pattern , doc):
            doc = re.sub(pattern, replace+suff, doc)

    return doc
