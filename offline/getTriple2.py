# 将DBpedia里的RDF三元组读取进来，urldecode之后，拆分成（主，谓，宾）写出去
import re
from urllib.parse  import unquote


def triple1(s):
  return s.split('/')[-1]
def triple2(s):
  if re.search(r'#',s):
    return s.split('#')[-1]
  else:
    return s.split('/')[-1]

def triple3(s):
  if re.search(r'#',s):
    return s.split('#')[-1]
  else:
    return s.split('/')[-1]
# file = open(r"./txt/image_en_sub.txt")
file = open(r"./txt/src/dbpedia/infoboxproperties_en.nt")
distArr=[]
line = file.readline()  
i=0
while line:
  # print(line)
  # lst=line.split(r" ")[0:3]
  lst=re.findall(r"<(.+?)>|\"(.*)\"",line)
  lst=list(map(lambda t:t[0] if t[0] else t[1],lst) )
  # print(lst)
  # break
  lst=list(map(lambda url:unquote(url),lst)) #解码
  # lst=list(map(lambda s:s.split('/')[-1],lst)) #挑出可读的部分
  lst[0]=triple1(lst[0])
  lst[1]=triple2(lst[1])
  lst[2]=triple3(lst[2])
  line=file.readline()
  distArr.append(str(lst)+'\n')
  # print(str(lst))
  # break
  i=i+1
  if i%100==0:
    print(i)
dist = open(r"./txt/dist/dbpedia/infoboxproperties_en.txt",'w')
dist.writelines(distArr)
dist.close()
