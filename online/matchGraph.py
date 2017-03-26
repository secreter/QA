 # 子图匹配算法，获取得分最高的k个子图

import json
import sys
import requests
sys.path.append("../offline")
from graphGenerate import getGraph
from getRelFromN import getTriple
from getEntityLinking import getEntity
from getRelPath import getRelPath
# 建立RDF图
# g=getGraph()
# 从句子中提取三元组
# sents="where does Aaron Kemps come from"
sents="What is Jordan's career?"
sents="What is Jordan?"
t=getTriple(sents)
if not t :
  print('getTriple failed!')
  exit()
arg1,rel,arg2=t
# 获取实体链接
arg1Lst=getEntity(arg1)
arg2Lst=getEntity(arg2)
# 获取谓词路径
relLst=getRelPath(rel)
if relLst[0][0]=='be':
  req=requests.get('http://localhost:5001/rdf?v='+arg1Lst[0])
  print(req.text)
  data=json.loads(req.text)
  print(data['name'])
  exit()

print('arg1Lst: '+str(arg1Lst))
print('arg2Lst: '+str(arg2Lst))
print('relLst: '+str(relLst))


# url='http://localhost:5003/rdf?v='+sub+'&e='+pathArr[0][0]
# req = requests.get(url)
# data=json.loads(req.text)
# answer=data['pointTo'].replace('resource/','')
# print(sents)
# print(answer)

