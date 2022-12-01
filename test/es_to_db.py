from elasticsearch import Elasticsearch
import pandas as pd # to make the data to dataframe
from sqlalchemy import create_engine # to connect DB

import torch, gc
gc.collect()
torch.cuda.empty_cache()

es = Elasticsearch('http://localhost:9199')

# 조회할 es 정보
index = 'kpf_bigkindslab_v1.1_2021'
body = {
    "_source": ["_id", "NewsItem.NewsComponent.NewsComponent.ContentItem.DataContent"],
    "query": {
        "match_all": {}
    }
}

# es 조회 결과값
res = es.search(
    index=index,
    # doc_type='doc',
    scroll='20m',
    size=500,
    body=body
)

# DB insert 위해 담아둘 arr
id_arr = []
conts_arr = []

# 대용량 처리
sid = res['_scroll_id']
size = res['hits']['total']['value']
while (size > 0):
    res = es.scroll(scroll_id= sid, scroll='20m')
    sid = res['_scroll_id']
    size = len(res['hits']['hits'])
    idx = 0
    for doc in res['hits']['hits']:
        id_arr.append(doc['_id'])
        conts_arr.append(doc['_source']['NewsItem']['NewsComponent']['NewsComponent'][0]['ContentItem']['DataContent'].replace("&quot;","\"").replace("&apos;","'"))
        if idx == 5:
            break
        idx += 1
    print(len(id_arr))
    print(len(conts_arr))
