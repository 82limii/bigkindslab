from flask import Flask, request, jsonify
from flask.templating import render_template
import pandas as pd

from predict_module import summarize_test
from baikal_tagger import nlp_tagger
from keyword_module import keyword_ext
from ner_module import ner_predict
from statistics_module import keyword_cnt, basic_statis, cor_statis, scatter

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 기사 요약 sentences : String , result : String Array
@app.route("/get_summary", methods=['POST'])
def summary():
    test_context = request.get_json()['sentences']
    rtn = summarize_test(test_context)
    response = dict()
    response['result'] = rtn # 결과 문자열

    return jsonify(response), 200

# 형태소 분석 text : String , result : JSON
@app.route("/get_tag", methods=['POST'])
def tag():
    test_context = request.get_json()['text']
    res = nlp_tagger(test_context)
    response = dict()
    response['result'] = res # 결과 문자열

    return jsonify(response), 200

# 키워드 추출 text : String , result : String Array    
@app.route("/get_keyword", methods=['POST'])
def keyword(): # 키워드 추출
    test_context = request.get_json()['text']
    rtn = keyword_ext(test_context)
    response = dict()
    response['result'] = rtn # 결과 문자열

    return jsonify(response), 200

#  text : String , result : String     
@app.route("/get_ner", methods=['POST'])
def ner(): # 개체명 인식
    test_context = request.get_json()['text']
    rtn = ner_predict(test_context)
    response = dict()
    response['result'] = rtn # 결과 문자열

    return jsonify(response), 200

# keywordList : String Array, startDt : String, endDt : String
# keyCnt : JSON, basicRes : Array, corRes : Array
@app.route("/get_basic_sta", methods=['POST'])
def basic_statis(): # 기초통계 및 상관관계 분석
    # request 값 가져오는 부분
    key_list = request.get_json()['keywordList']
    start_dt = request.get_json()['startDt']
    end_dt = request.get_json()['endDt']

    # 통계 분석 위해 필요한 데이터로 가공
    res_cnt = keyword_cnt(key_list, start_dt, end_dt)
    values_df = pd.DataFrame(res_cnt['keywordCnt'], index=res_cnt['dates'])

    # 기초통계 계산
    basic_res = basic_statis(key_list, values_df)
    # 상관관계 계산
    cor_res = cor_statis(key_list, values_df)
    response = dict()
    response['keyCnt'] = res_cnt
    response['basicRes'] = basic_res
    response['corRes'] = cor_res

    return jsonify(response), 200

# keyCnt : JSON, key1 : String, key2 : String
# cord : , lineRes :
@app.route("/get_scatter", methods=['POST'])
def scatter(): # 산점도 추출
    # request 값 가져오는 부분
    # 1안
    # key_list = request.get_json()['keywordList']
    # start_dt = request.get_json()['startDt']
    # end_dt = request.get_json()['endDt']
    # 2안
    res_cnt = request.get_json()['keyCnt']

    key1 = request.get_json()['key1']
    key2 = request.get_json()['key2']

    # 통계 분석 위해 필요한 데이터로 가공
    # res_cnt = keyword_cnt(key_list, start_dt, end_dt)
    values_df = pd.DataFrame(res_cnt['keywordCnt'], index=res_cnt['dates'])

    # 산점도
    cord, line_res = scatter(values_df, key1, key2)
    response = dict()
    response['cord'] = cord
    response['lineRes'] = line_res

    return jsonify(response), 200

#
@app.route("/get_regression", methods=['POST'])
def regression():  # 회귀분석 계산
    # request 값 가져오는 부분
    # 1안
    # key_list = request.get_json()['keywordList']
    # start_dt = request.get_json()['startDt']
    # end_dt = request.get_json()['endDt']
    # 2안
    res_cnt = request.get_json()['keyCnt']

    dep_nm = request.get_json()['depNm']

    # 통계 분석 위해 필요한 데이터로 가공
    # res_cnt = keyword_cnt(key_list, start_dt, end_dt)
    values_df = pd.DataFrame(res_cnt['keywordCnt'], index=res_cnt['dates'])

    # 산점도
    regres_table_res, regres_res = regression(values_df, dep_nm)
    response = dict()
    response['regreResTable'] = regres_table_res
    response['regreRes'] = regres_res

    return jsonify(response), 200

@app.route('/temp')
def temp():
    return render_template('input_test.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)