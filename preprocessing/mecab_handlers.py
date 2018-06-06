#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MeCab
m = MeCab.Tagger("-Ochasen")


def doc_to_words(doc, parts=None):
    
    '''
    mecab-pythonを使って文章から語句を分かち書きしてリストにする

    :param str doc: 文章
    :param list parts: このリストに含まれる品詞の語句のみを取り出す。デフォルト（None）は全ての品詞を返す。

    >>> doc_to_words("私は明日海へ行きます", ["名詞", "動詞"])
    '''

    ss = m.parse(doc)
    rows = ss.split("\n")
    split_rows = [row.split("\t") for row in rows]
    word_part_tups = [(split_row[0], split_row[3]) for split_row in split_rows if len(split_row)>=4]  # 語句とその品詞
    words = []
    if parts is None:
        for word, part in word_part_tups:
            words.append(word)
    else:
        for word, part in word_part_tups:
            exist_parts = part.split("-")
            matched_list = list(set(parts) & set(exist_parts))  # 語句の品詞と指定した品詞で共通するもの
            if len(matched_list) > 0:
                words.append(word)
    return(words)