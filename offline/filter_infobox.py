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
'longm','ign','gspot','jp','cero','esrb',
'pegi','oflca','_1up','gamepro','gspy',
'gt','np','mc','na','pal','usk','oflc',
'egm','fam','pjo']
with open(r"./txt/dist/dbpedia/infobox_en_filter.txt",'w',encoding='utf-8') as dist:
  while line:
    i=i+1
    line=file.readline()
    # 最后多了一个空行
    if line=='\n':
      continue
    try:
      lst=eval(line)
    except SyntaxError:
      print('SyntaxError in eval')
    # 过滤长度不为3的异常项
    if len(lst)!=3:
      continue
    # 过滤太长的
    if len(lst[0])>25 or len(lst[2])>25:
      continue
    # 必须以resource开头，不然后面不好处理，但这样是不合理的
    if not lst[0].startswith('resource/'):
      continue
    # print(lst)
    if lst[1] in dropArr:
      continue

    dist.write(str(lst)+'\n')
    
    if i%10000==0:
      print(i)
      # break

