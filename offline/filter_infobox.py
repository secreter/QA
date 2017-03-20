# 数据量太大，跑起来特别慢，过滤掉一些无用的
import re
from urllib.parse  import unquote


def triple1(s):
  return '/'.join(s.split('/')[-2:])
def triple2(s):
  if re.search(r'#',s):
    return s.split('#')[-1]
  else:
    return s.split('/')[-1]

def triple3(s):
  if re.search(r'http://',s):
    s='/'.join(s.split('/')[-2:])
  return s.replace('\\','')

file = open(r"./txt/dist/dbpedia/infobox_en.txt",'r',encoding='utf-8')
line = True 
i=0
dropArr=['id','img','label','url','wikiPageUsesTemplate',
'otheruses4Property','oclc','isbn','imgCapt',
'lowerCaption','misc','before','after','ratingProperty',
'lastAlbum','nextAlbum','latd','latm','latns','longd',
'longm']
with open(r"./txt/dist/dbpedia/infobox_en_filter.txt",'w',encoding='utf-8') as dist:
  while line:
    i=i+1
    line=file.readline()
    lst=eval(line)
    # 过滤长度不为3的异常项
    if len(lst)!=3:
      continue
    # print(lst)
    if lst[1] in dropArr:
      continue

    dist.write(str(lst)+'\n')
    
    if i%10000==0:
      print(i)
      # break

