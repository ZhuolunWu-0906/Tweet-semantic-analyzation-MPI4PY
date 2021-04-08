import json
import sys
import itertools
# wordfile = sys.argv[1]

def text_to_score(text,wordmark_d):
    mark = 0
    head=text.split()[:-1]
    foot=text.split()[1:]
    for i in range(len(head)):
        head[i]=head[i]+" "+foot[i]
    for i in head:
       if(i.rstrip("!,?.’”") in wordmark_d.keys()):
           mark += int(wordmark_d[i.rstrip("!,?.’”")])
           text=text.replace(i,'',1)
    for i in text.split():
       if(i.rstrip("!,?.’”") in wordmark_d.keys()):
           mark += int(wordmark_d[i.rstrip("!,?.’”")])
    return mark

text = open("tinyTwitter.json",'rb')
text_dict = json.load(text)
d= {}
# for i in text_dict['rows']:
#     print(i['value']['properties']['text'])

wordmark = open("AFINN.txt")
wordmark_d = {}
for line in wordmark:
    key, value = line.rsplit("	", 1)
    wordmark_d[key] = value.replace("\n", "")
# print (wordmark_d)

for i in text_dict['rows']:
    text = (i['value']['properties']['text'])
    mark = text_to_score(text,wordmark_d)
    print(mark)
