import sys
# from baikalnlpy import Tagger
from bareunpy import Tagger

tag_map = dict()

tag_map['NNG'] = '일반 명사'
tag_map['NNP'] = '고유 명사'
tag_map['NNB'] = '의존 명사'
tag_map['NP'] = '대명사'
tag_map['NR'] = '수사'
tag_map['NF'] = '명사 추정 범주'
tag_map['NA'] = '분석불능범주'
tag_map['NV'] = '용언 추정 범주'
tag_map['VV'] = '동사'
tag_map['VA'] = '형용사'
tag_map['VX'] = '보조 용언'
tag_map['VCP'] = '긍정 지정사'
tag_map['VCN'] = '부정 지정사'
tag_map['MMA'] = '성상 관형사'
tag_map['MMD'] = '지시 관형사'
tag_map['MMN'] = '수 관형사'
tag_map['MAG'] = '일반 부사'
tag_map['MAJ'] = '접속 부사'
tag_map['IC'] = '감탄사'
tag_map['JKS'] = '주격 조사'
tag_map['JKC'] = '보격 조사'
tag_map['JKG'] = '관형격 조사'
tag_map['JKO'] = '목적격 조사'
tag_map['JKB'] = '부사격 조사'
tag_map['JKV'] = '호격 조사'
tag_map['JKQ'] = '인용격 조사'
tag_map['JX'] = '보조사'
tag_map['JC'] = '접속 조사'
tag_map['EP'] = '선어말 어미'
tag_map['EF'] = '종결 어미'
tag_map['EC'] = '연결 어미'
tag_map['ETN'] = '명사형 전성 어미'
tag_map['ETM'] = '관형형 전성 어미'
tag_map['XPN'] = '체언 접두사'
tag_map['XSN'] = '명사 파생 접미사'
tag_map['XSV'] = '동사 파생 접미사'
tag_map['XSA'] = '형용사 파생 접미사'
tag_map['XR'] = '어근'
tag_map['SF'] = '마침표, 물음표, 느낌표'
tag_map['SP'] = '쉼표, 가운뎃점, 콜론, 빗금'
tag_map['SS'] = '따옴표, 괄호표, 줄표'
tag_map['SE'] = '줄임표'
tag_map['SO'] = '붙임표(물결, 숨김, 빠짐)'
tag_map['SW'] = '기타기호 (논리수학기호, 화폐기호)'
tag_map['SL'] = '외국어'
tag_map['SH'] = '한자'
tag_map['SN'] = '숫자'

def nlp_tagger(text):
    tagger = Tagger('gpu2.baikal.ai')

    pos = tagger.pos(text)
    res = tagger.tags(text)

    json_arr = []
    for pa in pos:
        json_data = dict()
        json_data['word'] = pa[0]
        json_data['pos'] = pa[1]
        json_data['desc'] = tag_map[pa[1]]
        json_arr.append(json_data)
    return json_arr
