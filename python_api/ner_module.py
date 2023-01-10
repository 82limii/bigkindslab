# %%
from transformers import AutoTokenizer
from transformers import BertForTokenClassification, logging
logging.set_verbosity_error()
import sys

text = "러시아군이 5일 수도 크이우와 오데사, 크리비리흐, 수미 등 우크라이나 전역에 대규모 미사일 공격을 가했습니다. 이날은 주요 7개국(G7)과 호주, 유럽연합(EU)의 러시아산 원유 가격 상한제가 시행된 첫날이었는데요. 우크라이나에 따르면 러시아가 이날 우크라이나 전역에 발사한 미사일은 70발에 달합니다."

tokenizer = AutoTokenizer.from_pretrained("./kpfbert")

# kor_model = BertForTokenClassification.from_pretrained("kor-BERT-ner")
# kor_model.to("cuda")
#predict(text, tokenizer, kor_model)

kpf_model = BertForTokenClassification.from_pretrained("./kpf-BERT-ner5")
# kpf_model.to("cuda")
#predict(text, tokenizer, kpf_model)
        
labels = [
    'B-AFA_ART_CRAFT',
    'B-AFA_DOCUMENT',
    'B-AFA_MUSIC',
    'B-AFA_PERFORMANCE',
    'B-AFA_VIDEO',
    'B-AFW_OTHER_PRODUCTS',
    'B-AFW_SERVICE_PRODUCTS',
    'B-AF_BUILDING',
    'B-AF_CULTURAL_ASSET',
    'B-AF_MUSICAL_INSTRUMENT',
    'B-AF_ROAD',
    'B-AF_TRANSPORT',
    'B-AF_WEAPON',
    'B-AM_AMPHIBIA',
    'B-AM_BIRD',
    'B-AM_FISH',
    'B-AM_INSECT',
    'B-AM_MAMMALIA',
    'B-AM_OTHERS',
    'B-AM_PART',
    'B-AM_REPTILIA',
    'B-AM_TYPE',
    'B-CV_ART',
    'B-CV_BUILDING_TYPE',
    'B-CV_CLOTHING',
    'B-CV_CULTURE',
    'B-CV_CURRENCY',
    'B-CV_DRINK',
    'B-CV_FOOD',
    'B-CV_FOOD_STYLE',
    'B-CV_FUNDS',
    'B-CV_LANGUAGE',
    'B-CV_LAW',
    'B-CV_OCCUPATION',
    'B-CV_POLICY',
    'B-CV_POSITION',
    'B-CV_PRIZE',
    'B-CV_RELATION',
    'B-CV_SPORTS',
    'B-CV_SPORTS_INST',
    'B-CV_SPORTS_POSITION',
    'B-CV_TAX',
    'B-CV_TRIBE',
    'B-DT_DAY',
    'B-DT_DURATION',
    'B-DT_DYNASTY',
    'B-DT_GEOAGE',
    'B-DT_MONTH',
    'B-DT_OTHERS',
    'B-DT_SEASON',
    'B-DT_WEEK',
    'B-DT_YEAR',
    'B-EV_ACTIVITY',
    'B-EV_FESTIVAL',
    'B-EV_OTHERS',
    'B-EV_SPORTS',
    'B-EV_WAR_REVOLUTION',
    'B-FD_ART',
    'B-FD_HUMANITIES',
    'B-FD_MEDICINE',
    'B-FD_OTHERS',
    'B-FD_SCIENCE',
    'B-FD_SOCIAL_SCIENCE',
    'B-LCG_BAY',
    'B-LCG_CONTINENT',
    'B-LCG_ISLAND',
    'B-LCG_MOUNTAIN',
    'B-LCG_OCEAN',
    'B-LCG_RIVER',
    'B-LCP_CAPITALCITY',
    'B-LCP_CITY',
    'B-LCP_COUNTRY',
    'B-LCP_COUNTY',
    'B-LCP_PROVINCE',
    'B-LC_OTHERS',
    'B-LC_SPACE',
    'B-MT_CHEMICAL',
    'B-MT_ELEMENT',
    'B-MT_METAL',
    'B-MT_ROCK',
    'B-OGG_ART',
    'B-OGG_ECONOMY',
    'B-OGG_EDUCATION',
    'B-OGG_FOOD',
    'B-OGG_HOTEL',
    'B-OGG_LAW',
    'B-OGG_LIBRARY',
    'B-OGG_MEDIA',
    'B-OGG_MEDICINE',
    'B-OGG_MILITARY',
    'B-OGG_OTHERS',
    'B-OGG_POLITICS',
    'B-OGG_RELIGION',
    'B-OGG_SCIENCE',
    'B-OGG_SPORTS',
    'B-PS_CHARACTER',
    'B-PS_NAME',
    'B-PS_PET',
    'B-PT_FLOWER',
    'B-PT_FRUIT',
    'B-PT_GRASS',
    'B-PT_OTHERS',
    'B-PT_PART',
    'B-PT_TREE',
    'B-PT_TYPE',
    'B-QT_ADDRESS',
    'B-QT_AGE',
    'B-QT_ALBUM',
    'B-QT_CHANNEL',
    'B-QT_COUNT',
    'B-QT_LENGTH',
    'B-QT_MAN_COUNT',
    'B-QT_ORDER',
    'B-QT_OTHERS',
    'B-QT_PERCENTAGE',
    'B-QT_PHONE',
    'B-QT_PRICE',
    'B-QT_SIZE',
    'B-QT_SPEED',
    'B-QT_SPORTS',
    'B-QT_TEMPERATURE',
    'B-QT_VOLUME',
    'B-QT_WEIGHT',
    'B-TI_DURATION',
    'B-TI_HOUR',
    'B-TI_MINUTE',
    'B-TI_OTHERS',
    'B-TI_SECOND',
    'B-TMIG_GENRE',
    'B-TMI_EMAIL',
    'B-TMI_HW',
    'B-TMI_MODEL',
    'B-TMI_PROJECT',
    'B-TMI_SERVICE',
    'B-TMI_SITE',
    'B-TMI_SW',
    'B-TMM_DISEASE',
    'B-TMM_DRUG',
    'B-TM_CELL_TISSUE_ORGAN',
    'B-TM_CLIMATE',
    'B-TM_COLOR',
    'B-TM_DIRECTION',
    'B-TM_SHAPE',
    'B-TM_SPORTS',
    'B-TR_ART',
    'B-TR_HUMANITIES',
    'B-TR_MEDICINE',
    'B-TR_OTHERS',
    'B-TR_SCIENCE',
    'B-TR_SOCIAL_SCIENCE',
    'I-AFA_ART_CRAFT',
    'I-AFA_DOCUMENT',
    'I-AFA_MUSIC',
    'I-AFA_PERFORMANCE',
    'I-AFA_VIDEO',
    'I-AFW_OTHER_PRODUCTS',
    'I-AFW_SERVICE_PRODUCTS',
    'I-AF_BUILDING',
    'I-AF_CULTURAL_ASSET',
    'I-AF_MUSICAL_INSTRUMENT',
    'I-AF_ROAD',
    'I-AF_TRANSPORT',
    'I-AF_WEAPON',
    'I-AM_AMPHIBIA',
    'I-AM_BIRD',
    'I-AM_FISH',
    'I-AM_INSECT',
    'I-AM_MAMMALIA',
    'I-AM_OTHERS',
    'I-AM_PART',
    'I-AM_REPTILIA',
    'I-AM_TYPE',
    'I-CV_ART',
    'I-CV_BUILDING_TYPE',
    'I-CV_CLOTHING',
    'I-CV_CULTURE',
    'I-CV_CURRENCY',
    'I-CV_DRINK',
    'I-CV_FOOD',
    'I-CV_FOOD_STYLE',
    'I-CV_FUNDS',
    'I-CV_LANGUAGE',
    'I-CV_LAW',
    'I-CV_OCCUPATION',
    'I-CV_POLICY',
    'I-CV_POSITION',
    'I-CV_PRIZE',
    'I-CV_RELATION',
    'I-CV_SPORTS',
    'I-CV_SPORTS_INST',
    'I-CV_SPORTS_POSITION',
    'I-CV_TAX',
    'I-CV_TRIBE',
    'I-DT_DAY',
    'I-DT_DURATION',
    'I-DT_DYNASTY',
    'I-DT_GEOAGE',
    'I-DT_MONTH',
    'I-DT_OTHERS',
    'I-DT_SEASON',
    'I-DT_WEEK',
    'I-DT_YEAR',
    'I-EV_ACTIVITY',
    'I-EV_FESTIVAL',
    'I-EV_OTHERS',
    'I-EV_SPORTS',
    'I-EV_WAR_REVOLUTION',
    'I-FD_ART',
    'I-FD_HUMANITIES',
    'I-FD_MEDICINE',
    'I-FD_OTHERS',
    'I-FD_SCIENCE',
    'I-FD_SOCIAL_SCIENCE',
    'I-LCG_BAY',
    'I-LCG_CONTINENT',
    'I-LCG_ISLAND',
    'I-LCG_MOUNTAIN',
    'I-LCG_OCEAN',
    'I-LCG_RIVER',
    'I-LCP_CAPITALCITY',
    'I-LCP_CITY',
    'I-LCP_COUNTRY',
    'I-LCP_COUNTY',
    'I-LCP_PROVINCE',
    'I-LC_OTHERS',
    'I-LC_SPACE',
    'I-MT_CHEMICAL',
    'I-MT_ELEMENT',
    'I-MT_METAL',
    'I-MT_ROCK',
    'I-OGG_ART',
    'I-OGG_ECONOMY',
    'I-OGG_EDUCATION',
    'I-OGG_FOOD',
    'I-OGG_HOTEL',
    'I-OGG_LAW',
    'I-OGG_LIBRARY',
    'I-OGG_MEDIA',
    'I-OGG_MEDICINE',
    'I-OGG_MILITARY',
    'I-OGG_OTHERS',
    'I-OGG_POLITICS',
    'I-OGG_RELIGION',
    'I-OGG_SCIENCE',
    'I-OGG_SPORTS',
    'I-PS_CHARACTER',
    'I-PS_NAME',
    'I-PS_PET',
    'I-PT_FLOWER',
    'I-PT_FRUIT',
    'I-PT_GRASS',
    'I-PT_OTHERS',
    'I-PT_PART',
    'I-PT_TREE',
    'I-PT_TYPE',
    'I-QT_ADDRESS',
    'I-QT_AGE',
    'I-QT_ALBUM',
    'I-QT_CHANNEL',
    'I-QT_COUNT',
    'I-QT_LENGTH',
    'I-QT_MAN_COUNT',
    'I-QT_ORDER',
    'I-QT_OTHERS',
    'I-QT_PERCENTAGE',
    'I-QT_PHONE',
    'I-QT_PRICE',
    'I-QT_SIZE',
    'I-QT_SPEED',
    'I-QT_SPORTS',
    'I-QT_TEMPERATURE',
    'I-QT_VOLUME',
    'I-QT_WEIGHT',
    'I-TI_DURATION',
    'I-TI_HOUR',
    'I-TI_MINUTE',
    'I-TI_OTHERS',
    'I-TI_SECOND',
    'I-TMIG_GENRE',
    'I-TMI_EMAIL',
    'I-TMI_HW',
    'I-TMI_MODEL',
    'I-TMI_PROJECT',
    'I-TMI_SERVICE',
    'I-TMI_SITE',
    'I-TMI_SW',
    'I-TMM_DISEASE',
    'I-TMM_DRUG',
    'I-TM_CELL_TISSUE_ORGAN',
    'I-TM_COLOR',
    'I-TM_DIRECTION',
    'I-TM_SHAPE',
    'I-TM_SPORTS',
    'I-TR_ART',
    'I-TR_HUMANITIES',
    'I-TR_MEDICINE',
    'I-TR_OTHERS',
    'I-TR_SCIENCE',
    'I-TR_SOCIAL_SCIENCE',
    'O',
]

label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}

def ner_predict(text):
    model = kpf_model
    
    text = text.replace(" ", "-")
    test_tokenized = tokenizer(text, return_tensors="pt")

    test_input_ids = test_tokenized["input_ids"]
    test_attention_mask = test_tokenized["attention_mask"]
    test_token_type_ids = test_tokenized["token_type_ids"]

    inputs = {
        "input_ids" : test_input_ids,
        "attention_mask" : test_attention_mask,
        "token_type_ids" : test_token_type_ids
    }

    outputs = model(**inputs)
    token_predictions = outputs[0].argmax(dim=2)
    token_prediction_list = token_predictions.squeeze(0).tolist()

    pred_str = [id2label[l] for l in token_prediction_list]
    tt_tokenized = tokenizer(text).encodings[0].tokens

    decoding_ner_sentence = ""
    is_prev_entity = False
    prev_entity_tag = ""
    is_there_B_before_I = False
    for i, (token, pred) in enumerate(zip(tt_tokenized, pred_str)):
        if i == 0 or i == len(pred_str) - 1:
            continue
        token = token.replace('#', '').replace("-", " ")

        if 'B-' in pred:
            if is_prev_entity is True:
                decoding_ner_sentence += ':' + prev_entity_tag+ '>'

            if token[0] == ' ':
                token = list(token)
                token[0] = ' <'
                token = ''.join(token)
                decoding_ner_sentence += token
            else:
                decoding_ner_sentence += '<' + token
            is_prev_entity = True
            prev_entity_tag = pred[2:]
            is_there_B_before_I = True

        elif 'I-' in pred:
            decoding_ner_sentence += token

            if is_there_B_before_I is True:
                is_prev_entity = True
        else:
            if is_prev_entity is True:
                decoding_ner_sentence += ':' + prev_entity_tag+ '>' + token
                is_prev_entity = False
                is_there_B_before_I = False
            else:
                decoding_ner_sentence += token
                
    return decoding_ner_sentence
