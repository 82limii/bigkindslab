from flask import Flask, request, jsonify
from flask.templating import render_template

from predict_module import summarize_test
from baikal_tagger import nlp_tagger
from keyword_module import keyword_ext
from ner_module import ner_predict

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 기사 요약 sentences : String , result : String Array
@app.route("/get_summary", methods=['POST'])
def summary():
    test_context = request.form['sentences']
    rtn = summarize_test(test_context)
    response = dict()
    response['result'] = rtn # 결과 문자열

    return jsonify(response), 200

# 형태소 분석 text : String , result : JSON
@app.route("/get_tag", methods=['POST'])
def tag():
    test_context = request.form['text']
    res = nlp_tagger(test_context)
    response = dict()
    response['result'] = res # 결과 문자열

    return jsonify(response), 200

# 키워드 추출 text : String , result : String Array    
@app.route("/get_keyword", methods=['POST'])
def keyword(): # 키워드 추출
    test_context = request.form['text']
    rtn = keyword_ext(test_context)
    response = dict()
    response['result'] = rtn # 결과 문자열

    return jsonify(response), 200

#  text : String , result : String     
@app.route("/get_ner", methods=['POST'])
def ner(): # 개체명 인식
    test_context = request.form['text']
    rtn = ner_predict(test_context)
    response = dict()
    response['result'] = rtn # 결과 문자열

    return jsonify(response), 200

@app.route('/temp')
def temp():
    return render_template('input_test.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)