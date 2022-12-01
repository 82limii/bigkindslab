# %%
import json
import xmltodict

with open("../data/01100201.20200101000125001.xml",'r', encoding='utf-8') as f:
    xmlString = f.read()

print("xml input (xml_to_json.xml):")
print(xmlString)

# %%
jsonDump = xmltodict.parse(xmlString)['NewsML']

print("\nJSON output(output.json):")
print(jsonDump)

# %%
jsonString = json.dumps(xmltodict.parse(xmlString)['NewsML'], indent=4)

print("\nJSON output(output.json):")
print(jsonString)

with open("01100201.20200101000125001.json", 'w') as f:
    f.write(jsonString)

# %%
from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch('http://localhost:9199')

request_body = {
    "settings" : {
        "number_of_shards": 6,
        "number_of_replicas": 1
    }
}
es.indices.create(index = 'example_index', body = request_body)

bulk_data = []

# for index, row in data_for_es.iterrows():
#     data_dict = {}
#     for i in range(len(row)):
#         data_dict[data_for_es.columns[i]] = row[i]
#     op_dict = {
#         "index": {
#             "_index": 'example_index',
#             "_type": 'examplecase',
#             "_id": data_dict['some_PK']
#         }
#     }
#     bulk_data.append(op_dict)
#     bulk_data.append(data_dict)

# %%
# doc = {
#     "category" : "skirt",
#     "c_key" : "1234",
#     "price" : 11400,
#     "status" : 1,
#     "@timestamp" : datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
# }

es.index(index="example_index", doc_type="_doc", body=jsonString, id='01100201.20200101000125001')
