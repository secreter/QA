# 将DBpedia里的RDF三元组读取进来，urldecode之后，拆分成（主，谓，宾）写出去
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

# file = open(r"./txt/image_en_sub.txt")
file = open(r"./txt/src/dbpedia/infobox_en.nt",'r',encoding='utf-8')
distArr=[]
line = file.readline()  
i=0
with open(r"./txt/dist/dbpedia/infobox_en.txt",'w',encoding='utf-8') as dist:
  while line:
    lst=re.findall(r"<(.+?)>|\"(.*)\"",line)
    lst=list(map(lambda t:t[0] if t[0] else t[1],lst) )
    lst=list(map(lambda url:unquote(url),lst)) #解码
    lst[0]=triple1(lst[0])
    lst[1]=triple2(lst[1])
    lst[2]=triple3(lst[2])
    line=file.readline()
    dist.write(str(lst)+'\n')
    # print(str(lst))
    # break
    i=i+1
    if i%100000==0:
      print(i)
      # break 

