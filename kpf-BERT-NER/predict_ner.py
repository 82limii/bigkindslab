###########################################################################################################
"""
Predict.py : 추론 관련 코드.
- 실행하는 폴더에 predict.py, label.py, kpf-bert, kpf-bert-ner, kor-bert-ner 폴더가 있어야함.
- 입력 형태 : python predict.py FILE
input : FILE (sentence)
output : word, label, desc (predict results using kor-bert-ner, kpf-bert-ner)
"""
###########################################################################################################

from transformers import AutoTokenizer, BertForTokenClassification, logging
logging.set_verbosity_error()
import sys
import label
import kss

#############################################################################################################
"""
    predict(text, tokenizer, model) : 추론 함수.
    - 문장을 입력받아 model input 에 맞게 변환.
    - model에 입력 후 추론 클래스들을 output으로 반환.
    input : text (text를 tokneizer한 결과물을 넣음)
    output : word, label, desc (dict형태로 토큰에 대한 결과 반환)
"""
###############################################################################################################
def predict(text, tokenizer, model):
    text = text.replace('\n','')

    sents = kss.split_sentences(text)
    decoding_ner_sentence = ""
    word_list = list()

    #text to model input
    for sent in sents:

        sent = sent.replace(" ", "-")
        test_tokenized = tokenizer(sent, return_tensors="pt")

        test_input_ids = test_tokenized["input_ids"]
        test_attention_mask = test_tokenized["attention_mask"]
        test_token_type_ids = test_tokenized["token_type_ids"]

        inputs = {
            "input_ids" : test_input_ids,
            "attention_mask" : test_attention_mask,
            "token_type_ids" : test_token_type_ids
        }
        #predict
        outputs = model(**inputs)

        token_predictions = outputs[0].argmax(dim=2)
        token_prediction_list = token_predictions.squeeze(0).tolist()

        pred_str = [label.id2label[l] for l in token_prediction_list]
        tt_tokenized = tokenizer(sent).encodings[0].tokens

        # decoding_ner_sentence = ""
        is_prev_entity = False
        prev_entity_tag = ""
        is_there_B_before_I = False
        _word = ""
        # word_list = list()
    
        #model output to text
        for i, (token, pred) in enumerate(zip(tt_tokenized, pred_str)):
            if i == 0 or i == len(pred_str) - 1:
                continue
            token = token.replace('#', '').replace("-", " ")

            if 'B-' in pred:
                if is_prev_entity is True:
                    decoding_ner_sentence += ':' + prev_entity_tag+ '>'
                    word_list.append({"word" : _word, "label" : prev_entity_tag, "desc" : "1"})
                    _word = ""

                if token[0] == ' ':
                    token = list(token)
                    token[0] = ' <'
                    token = ''.join(token)
                    decoding_ner_sentence += token
                    _word += token
                else:
                    decoding_ner_sentence += '<' + token
                    _word += token
                is_prev_entity = True
                prev_entity_tag = pred[2:]
                is_there_B_before_I = True

            elif 'I-' in pred:
                decoding_ner_sentence += token
                _word += token

                if is_there_B_before_I is True:
                    is_prev_entity = True
            else:
                if is_prev_entity is True:
                    decoding_ner_sentence += ':' + prev_entity_tag+ '>' + token
                    is_prev_entity = False
                    is_there_B_before_I = False
                    word_list.append({"word" : _word, "label" : prev_entity_tag, "desc" : label.ner_code[prev_entity_tag]})
                    _word = ""
                else:
                    decoding_ner_sentence += token
                
    print("OUTPUT")
    print("sentence : ", decoding_ner_sentence)
    print("result : ", word_list)

##################################################################################################################
"""
    추론 함수를 실행하는 메인 함수.
    - 입력 형태 : python predict.py FILE
    - FILE의 문장을 kpf-bert-ner 모델과 kor-bert-ner 모델에 넣고 해당 결과를 출력.
"""
####################################################################################################################

if __name__ == "__main__":
    
    # if len(sys.argv) is 1:
    #     print("FILE을 입력해주세요.")
    # file_name = sys.argv[1]
    file_name = "./test.txt"
    f = open(file_name, 'rt', encoding="UTF8")
    s = f.read()
    print("TEXT input")
    print(s, "\n")
    f.close()
    
    #kor-bert-model load
    print("KOR-BERT-NER MODEL Loading...")
    kor_model = BertForTokenClassification.from_pretrained("./kor-BERT-ner")
    print("KOR-BERT-NER MODEL Loading Done")
    
    #kpf-bert-model load
    print("KPF-BERT-NER MODEL Loading...")
    kpf_model = BertForTokenClassification.from_pretrained("./kpf-BERT-ner")
    print("KPF-BERT-NER MODEL Loading Done")
    
    #kpf-bert tokenizer load
    print("KPF-BERT TOKENIZER Loading...")
    tokenizer = AutoTokenizer.from_pretrained("./kpfbert")
    print("KPF-BERT TOKENIZER Loading Done")
    print()
    
    text = s
    
    #predict using kor_model
    kor_model
    print("KOR MOEL Results")
    predict(text, tokenizer, kor_model)
    
    print()
    
    #predict using kpf_model
    kpf_model
    print("KPF MOEL Results")
    predict(text, tokenizer, kpf_model)