import sys
from baikalnlpy import Tagger

def nlp_tagger(text):
    tagger = Tagger()

    pos = tagger.pos(text)

    json_arr = []
    for pa in pos:
        json_data = dict()
        json_data['word'] = pa[0]
        json_data['pos'] = pa[1]
        json_arr.append(json_data)
    return json_arr
