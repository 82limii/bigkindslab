import json
import xmltodict
from datetime import datetime as dt

def make_json(xml_dir):
    with open(xml_dir,'r', encoding='utf-8') as f:
        xmlString = f.read()

    jsonDump = xmltodict.parse(xmlString, attr_prefix='', cdata_key='text')
    jsonDump = jsonDump['NewsML']
    jsonDump['@timestamp'] = dt.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    jsonDump['NewsItem']['NewsComponent']['AdministrativeMetadata']['Provider']['Comment'] = jsonDump['NewsItem']['NewsComponent']['AdministrativeMetadata']['Provider']['Comment']['text']

    # json 파일 저장 필요할 경우 사용
    # dir_arr = xml_dir.split('/')
    # xml_name = dir_arr[len(dir_arr)-1]
    # jsonString = json.dumps(jsonDump, indent=4)
    # with open(xml_name.replace(".xml",".json"), 'w') as f:
    #     f.write(jsonString)
    
    return jsonDump