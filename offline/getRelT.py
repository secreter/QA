# 获取关系词典T，并倒排记录包含它的patternid
# 
import re
import json
file = open(r"./txt/dist/patty/wikipedia-patterns_filter.txt",'r',encoding='utf-8')
line = True 
# 用来存储关系短语关于patternid的倒排字典
dic={}
i=0
with open(r"./txt/dist/my/relT.txt",'w',encoding='utf-8') as dist:
  while line:
    i=i+1
    line=file.readline()
    # 最后多了一个空行
    if line=='\n' or line=='':
      continue
    lst=eval(line)
    # print(lst)
    arr=lst[1].split(';$')[:-1]
    # print(arr)
    for item in arr:
      if item not in dic:
        dic[item]=[] #初始化一个空数组
      dic[item].append(lst[0]) #记录倒排id

    if i%1000==0:
      print(i)
      # break
  json.dump(dic,dist)