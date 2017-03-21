# 将实体对根据id建立倒排字典，放在同一行
import re
file = open(r"./txt/src/patty/wikipedia-instances.txt",'r',encoding='utf-8')
dic={}
line = file.readline()  
i=0
with open(r"./txt/dist/patty/wikipedia-instances.txt",'w',encoding='utf-8') as dist:
  while line:
    i=i+1
    line = file.readline() 
    line=line[:-1]   # 去除\n
    if not line:   # empty
      continue 
    # print(line)
    lst=line.split('\t')
    if lst[0] not in dic:
      dic[lst[0]]=[]
    dic[lst[0]].append(str(lst[1:]))

    # print(lst)
    # print(dic)
    if i%10000==0:
      print(i)
      # break

  for key in dic:
    lst=dic[key]
    # id 和实体对之间用三个制表符，实体对之间用一个
    dist.write(key+'\t\t\t'+'\t'.join(lst)+'\n')
    # print(key)
