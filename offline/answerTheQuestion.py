# 进行图匹配找到答案
from getRelFromN import getTriple
import json
import requests

# 根据谓词短语查询到patternid
fRelT=open('./txt/dist/my/relT.txt','r',encoding='utf-8')
relT=json.load(fRelT)
# 根据patternid查询谓词路径path
fPaths=open('./txt/dist/my/paths_tf-idf.txt','r',encoding='utf-8')
paths=json.load(fPaths)

# sents="where does Aaron Kemps come from?"
sents="where is Hurricane Joe?"
sub,rel,obj=getTriple(sents)
print(rel)
print(relT[rel])
# 多个数组合并
pathArr=[]
for pid in relT[rel]:
  if pid in paths:
    pathArr+=paths[pid]

if len(pathArr)>3:
  # 排序并取top-3
  pathArr=sorted(pathArr,key=(lambda x:x[1]), reverse=True)[:3]
else:
  pathArr=sorted(pathArr,key=(lambda x:x[1]), reverse=True)

print(pathArr)

url='http://localhost:5003/rdf?v='+sub+'&e='+pathArr[0][0]
req = requests.get(url)
data=json.loads(req.text)
answer=data['pointTo'].replace('resource/','')
print(sents)
print(answer)

