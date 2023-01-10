from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
import pandas as pd
from scipy import stats
import numpy as np
from statsmodels.formula.api import ols

# 기간내 날짜 리스트
def date_range(start, end):
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    dates = [(start + timedelta(days=i)).strftime("%Y%m%d") for i in range((end-start).days+1)]
    return dates

# es 뉴스 건수 검색
def search_cnt(keyword,date):
    es = Elasticsearch('http://localhost:9199')
    index = 'kpf_bigkindslab_'+date[:4]
    body = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {
                        "type": "phrase_prefix",
                        "query": keyword,
                        "fields": ["headLine", "content", "subHeadLine"]
                    }},
                    {"multi_match": {
                        "query":date,
                        "fields": ["date"]
                    }}
                ]
            }
        }
    }
    res = es.count(index=index, body=body)
    return res['count']

# 키워드별 기사 건수 추출 메소드
def keyword_cnt(key_list, stDt, endDt):
    result = dict()  # java 단으로 넘길 데이터
    date_list = date_range(stDt,endDt)
    cnt = dict()
    for key in key_list:
        cnt_list = []
        for date in date_list:
            res = search_cnt(key, date)
            cnt_list.append(res)

        cnt[key] = cnt_list

    result['dates'] = date_list
    result['keywordCnt'] = cnt
    return result

# 기초통계 결과
def basic_statis(key_list, df):
    basic_res = []
    for key in key_list:
        val_dict = dict()
        val_dict['key'] = key
        val_dict['count'] = int(df.count()[key])
        val_dict['sum'] = int(df.sum()[key])
        val_dict['mean'] = float(df.mean()[key])
        val_dict['min'] = int(df.min()[key])
        val_dict['median'] = float(df.median()[key])
        val_dict['max'] = int(df.max()[key])
        val_dict['var'] = float(df.var()[key])
        val_dict['std'] = float(df.std()[key])
        basic_res.append(val_dict)
    return basic_res

# 상관관계 결과
def cor_statis(key_list, df):
    cor_res = []
    n = 0
    for key in key_list:
        for val in df[key]:
            n += val
    for key1 in key_list:
        for key2 in key_list:
            pear_cor = stats.pearsonr(df[key1], df[key2])
            cor_dict = dict()
            cor_dict['key1'] = key1
            cor_dict['key2'] = key2
            cor_dict['Pearson'] = float(pear_cor[0])
            cor_dict['pval'] = float(pear_cor[1])
            cor_dict['N'] = n
            cor_res.append(cor_dict)
    return cor_res

# 산점도
def scatter(df, key1, key2):
    cord = dict()
    lineRes = dict()
    z = np.polyfit(values_df[key1], values_df[key2], 1)
    f = np.poly1d(z)
    cord['x'] = values_df[key1].to_list()
    cord['y'] = values_df[key2].to_list()
    slope = z[0]
    intercept = z[1]
    lineRes['slope'] = slope
    lineRes['intercept'] = intercept
    return cord, lineRes

# 회귀분석
def regression(df, dep_nm):
    regre_res = dict()
    regre_table_res = []

    dep_val = ''  # 종속변수
    indep_val = ''  # 독립변수

    for col in values_df.columns:
        if col == dep_nm:
            dep_val += col + '~'
        else:
            indep_val += '+' + col

    str = dep_val + indep_val[1:]
    model = ols(str, data=values_df).fit()

    rsqu = model.rsquared
    rsqu_double = rsqu * rsqu
    fval = model.fvalue
    f_pval = model.f_pvalue
    dw = pd.read_html(model.summary().tables[2].as_html())[0][3][0]

    regre_res['rsqu'] = rsqu
    regre_res['rsqu_double'] = rsqu_double
    regre_res['fval'] = fval
    regre_res['f_pval'] = f_pval
    regre_res['dw'] = dw

    regre_table_res = []

    b = model.params  # 비표준화계수 B
    bse = model.bse  # 표준오차
    tval = model.tvalues  # t
    t_pval = model.pvalues  # 유의확률

    col_arr = indep_val[1:].split("+")

    for i in range(len(b)):
        if i == 0:
            continue
        regre_table = dict()
        regre_table['col'] = col_arr[i - 1]
        regre_table['b'] = b[i]  # B
        regre_table['bse'] = bse[i]  # 표준오차
        regre_table['tval'] = tval[i]  # t
        regre_table['t_pval'] = t_pval[i]  # 유의확률
        regre_table_res.append(regre_table)

    return regre_table_res, regre_res


if __name__ == "__main__":
    key_list = ['대선', '국민의', '윤석열']
    res = keyword_cnt(key_list, '20220309', '20220410')
    print(type(res['dates']))
    print(type(res['keywordCnt']))
    values_df = pd.DataFrame(res['keywordCnt'], index=res['dates'])
    basic_res = basic_statis(key_list, values_df)
    print(basic_res)
    print(type(basic_res[0]['count']))
    print(type(basic_res[0]['sum']))
    print(type(basic_res[0]['mean']))
    print(type(basic_res[0]['min']))
    print(type(basic_res[0]['median']))
    print(type(basic_res[0]['max']))
    print(type(basic_res[0]['var']))
    print(type(basic_res[0]['std']))
    cor_res = cor_statis(key_list, values_df)
    # print(type(res))
    # print(type(basic_res))
    # print(type(cor_res))
    print(cor_res)
    print(type(cor_res[0]['Pearson']))
    print(type(cor_res[0]['pval']))
    print(type(cor_res[0]['N']))
    # cord, lineRes = scatter(values_df, '대선', '국민의')
    # print(cord)
    # print(lineRes)
    # regre_table_res, regre_res = regression(values_df, '대선')
    # print(regre_res)
    # print(regre_table_res)
