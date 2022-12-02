from elasticsearch import Elasticsearch
from transform_module import make_json

es = Elasticsearch('http://localhost:9199')

mapping = {
    "settings" : {
        "number_of_shards": 6,
        "number_of_replicas": 1
    }
}

def insert_doc(xml_path):
    json_dict = make_json(xml_path) # xml_path에 해당 xml이 없을경우 에러처리 필요

    index = "kpf_bigkindslab_v1.1_" + json_dict['NewsEnvelope']['DateAndTime'][:4]
    news_id = json_dict['NewsItem']['Identification']['NewsIdentifier']['NewsItemId']

    # index가 존재하는 지 확인
    # index 없을 경우 index 생성 후 doc 추가
    if es.indices.exists(index=index) == False:
        es.indices.create(index=index, body=mapping)

    result = es.index(index=index, doc_type="_doc", body=json_dict, id=news_id)

    return result['_id'], result['_index']

def delete_doc(news_id):
    index = 'kpf_bigkindslab_v1.1_' + news_id.split(".")[1][:4]
    del_body = {
        "query": {
            "match": {
                "_id": news_id
            }
        }
    }
    result = es.delete_by_query(index=index, doc_type="_doc", body=del_body)

    # result['deleted'] == 0 : doc삭제되지 않음
    # result['deleted'] == 1 : doc삭제됨
    return result['deleted'], index