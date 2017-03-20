import json
import re
file = open(r"./txt/src/patty/wikipedia-patterns.txt",'r',encoding='utf-8')
distDict={}
line = file.readline()  
i=0
with open(r"./txt/src/patty/format-patterns.txt",'w',encoding='utf-8') as dist:
  while line:
    # lst=re.findall(r"<(.+?)>|\"(.*)\"",line)
    # lst=list(map(lambda t:t[0] if t[0] else t[1],lst) )
    # lst=list(map(lambda url:unquote(url),lst)) #解码
    # lst[0]=triple1(lst[0])
    # lst[1]=triple2(lst[1])
    # lst[2]=triple3(lst[2])
    line=file.readline()
    # dist.write(str(lst)+'\n')
    # print(line)
    lst=line.split('\t')
    # print(lst)
    distDict[lst[0]]={}
    if len(lst)<3:
        continue
    # 过滤开头和结尾的[[]]
    lst[1]=re.sub(r'^\[\[.*?\]\] ','',lst[1])
    lst[1]=re.sub(r';\$\[\[.*?\]\] | \[\[.*?\]\];\$',';$',lst[1])
    distDict[lst[0]]['patterns']=lst[1].split(';$')[:-1]
    distDict[lst[0]]['confidence']=lst[2]
    # print(lst[1])
    # break
    i=i+1
    if i%1000==0:
      print(i)
      # break

  distJson=json.dumps(distDict)
  dist.write(distJson)
