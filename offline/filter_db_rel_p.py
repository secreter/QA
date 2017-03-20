# 过滤dbpedia-relation-paraphrases.txt里的rel开头和结尾的
# [[]],中间的我们不过滤，因为这个里面是词性，本次初级阶段不考虑词性
# 中间的[[]]就匹配任意单词

import re
file = open(r"./txt/src/patty/dbpedia-relation-paraphrases.txt",'r',encoding='utf-8')
line = True 
i=0
with open(r"./txt/dist/patty/dbpedia-relation-paraphrases.txt",'w',encoding='utf-8') as dist:
  while line:
    line=file.readline()
    lst=line.split('\t')
    if len(lst)<2:
      continue
    lst[1]=re.sub(r'^\[\[.*?\]\] ','',lst[1]) #替换句首的【【】】
    lst[1]=re.sub(r' \[\[.*?\]\];\n$',';\n',lst[1]) #替换句尾的【【】】
    dist.write(''.join(lst))
    # print(lst)
    i=i+1
    if i%1000==0:
      print(i)
      # break