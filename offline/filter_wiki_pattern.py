# 过滤原生的wikipedia-patterns文件，只要patternid  patterntext 
# 字段，confidence感觉其实有用，不过暂时不要了
# 另外过滤pattern里的开头和结尾处的[[*]]

import re
file = open(r"./txt/src/patty/wikipedia-patterns.txt",'r',encoding='utf-8')
line = file.readline() 
i=0
with open(r"./txt/dist/patty/wikipedia-patterns_filter.txt",'w',encoding='utf-8') as dist:
  while line:
    i=i+1
    line=file.readline()
    # 最后多了一个空行
    if line=='\n' or line=='':
      continue
    lst=line.split('\t')[:2]
    # print(lst)
    lst[1]=re.sub(r'^\[\[\w*?\]\] ','',lst[1]) #替换句首的【【】】
    lst[1]=re.sub(r';\$\[\[\w*?\]\] ',';$',lst[1]) #替换句首的【【】】
    lst[1]=re.sub(r' \[\[\w*?\]\];\$',';$',lst[1]) #替换句尾的【【】】
    # print(lst)
    dist.write(str(lst)+'\n')
    if i%1000==0:
      print(i)
      # break