# -*- coding: utf-8 -*- 
# 将DBpedia里的RDF三元组读取进来，urldecode之后，拆分成（主，谓，宾）写出去
import re
from urllib.parse  import unquote
import codecs
i=0

# file = open(r"./txt/image_en_sub.txt")
file = open(r"./txt/src/dbpedia/image_en.nt")
with open(r"./txt/dist/dbpedia/image_en.txt",'w',encoding='utf-8') as dist:
  distArr=[]
  line = file.readline()  
  while line:
    # print(line)
    lst=re.findall(r"<(.+?)>",line)
    lst=list(map(lambda url:unquote(url),lst)) #解码
    # lst=list(map(lambda s:s.split('/')[-1],lst)) #挑出可读的部分
    lst[0]=lst[0].split('/')[-1]
    lst[1]=lst[1].split('/')[-1]
    lst[2]=lst[2]
    line=file.readline()
    # distArr.append(str(lst)+'\n')
    dist.write(str(lst)+'\n')
    # print(str(lst))
    i=i+1
    if i%100000==0:
      print(i)
      # break

# dist = codecs.open(r"./txt/dist/dbpedia/image_en.txt",'w','utf-8')
# dist.writelines(distArr)
# dist.close()
