# 将dbpedia-relation-paraphrases文件中的关系-模式 转换为关系短语词典D
# 存储为json格式
import json
import re
def hump2blank(s):
  """驼峰的字符串转换为空格分隔的"""
  newS=''
  for ch in s:  
    newS += ch if ch.islower() else ' '+ch.lower()
  return newS
def filte(s):
  """去除字符串里的[[]]"""
  s=re.sub( r'\[\[.+\]\]', '', s )
  return s.strip()

file = open(r"D:\study\school\classes\graduatepaper\data\patty-dataset\dbpedia-relation-paraphrases.txt")
dic={}        #dict
line = file.readline()             # 调用文件的 readline()方法
i=0
# 第一行是列名，跳过
while line:
  
  line = file.readline()
  lst=line.split('\t')
  # 最后一行是空行
  if(len(lst)<2):
    continue
  key=hump2blank(lst[0])
  val=filte(lst[1][:-2])
  if key in dic.keys():
    dic[key].append(val)
  else:
    dic[key]=[]
    dic[key].append(val)
  # print(dic)
  # print(dic)
  # i=i+1
  # if i>2:
  #   break

file.close()
f = open(r".\txt\rel_dic.txt",'w')
f.write(json.dumps(dic))
# 
# b'prospectTeam\tbeen playing with;\n'
# print(dic)
# print(hump2blank('prospectTeam'))