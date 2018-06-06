#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def split_by_sentence(doc, stopwords):
    
    '''
    文章を文単位に分割する

    :param list stopwords: 文末・文頭の記号
    :param str replace: 置き換える言葉

    >>> doc = 
    '''

    temp_re = "["
    for stopword in stopwords:
        temp_re += stopword
    temp_re += "]"

    sentences = re.split(temp_re, doc)
    sentences_cheched = []
    for s in sentences:
        if (s == "") or (s == " ") or (s=="　"):
            continue
        else:
            sentences_cheched.append(s)
    if len(sentences_cheched) == 0:
        sentences_cheched = [""]
    return sentences_cheched