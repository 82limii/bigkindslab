import xml.etree.ElementTree as ET

filePath = "../data/01100201.20200101000125001.xml"
tree = ET.parse(filePath)
root = tree.getroot()

date_time = root.find('NewsEnvelope').find('DateAndTime').text
date_time = date_time.replace('T','').split('+')[0]

item = root.find('NewsItem')
news_id = item.find('Identification').find('NewsIdentifier').find('NewsItemId').text
first_created = item.find('NewsManagement').find('FirstCreated').text
first_created = first_created.replace('T','').split('+')[0]

news_compo = item.find('NewsComponent')
news_lines = news_compo.find('NewsLines')
head_line = news_lines.find('HeadLine').text
by_line = news_lines.find('ByLine').text

admin_meta = news_compo.find('AdministrativeMetadata')
file_name = admin_meta.find('FileName').text
provider_name = admin_meta.find('Provider').find('Comment').text
provider_code = admin_meta.find('Provider').find('Party').get('FormalName')

meta = news_compo.find('Metadata')
props = meta.findall('Property')

provider_sub = ''
auto_sub = ''
for prop in props:
    if prop.get('FormalName') == 'SubjectInfo':
        provider_sub += prop.get('Value') + '|'
    if prop.get('FormalName') == 'SubjectInfo1':
        provider_sub += prop.get('Value') + '|'
    if prop.get('FormalName') == 'AutoSubjectInfo':
        auto_sub = prop.get('Value')
provider_sub = provider_sub[:-1]

news_compo_arr = news_compo.findall('NewsComponent')
data_cont = news_compo_arr[0].find('ContentItem').find('DataContent').text
data_html = news_compo_arr[1].find('ContentItem').find('DataContent').text
# data_html = data_html.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"')

data = dict()
data['date_time'] = date_time
data['news_id'] = news_id
data['first_created'] = first_created
data['head_line'] = head_line
data['by_line'] = by_line
data['file_name'] = file_name
data['provider_name'] = provider_name
data['provider_code'] = provider_code
data['provider_sub'] = provider_sub
data['auto_sub'] = auto_sub
data['data_cont'] = data_cont
data['data_html'] = data_html

print(data)