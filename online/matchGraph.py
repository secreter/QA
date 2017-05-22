 # 子图匹配算法，获取得分最高的k个子图

import json
import sys
import requests
sys.path.append("../offline")
from graphGenerate import getGraph
from getRelFromN import getTriple
from getEntityLinking import getEntity
from getRelPath import getRelPath

# 假设我们这里的arg1和arg2里，必有一个是只包含疑问代词的
# 那么我们就用另一个列表里的实体作为g里字典的key来搜索点
def getResourceLst(arg1Lst,arg2Lst):
  whArr=['when','where','why','who','which','what','how']
  # 疑问词直接返回（统一小写）
  if arg1Lst[0].lower() in whArr:
    lst=arg2Lst
  else:
    lst=arg1Lst
  return list(map(lambda s:'resource/'+s.replace(' ','_'),lst))

def edgeToPoint(v,edgeStr):
  """获取v开始，经过edgestr到达的点，如果这条边存在的话"""
  e=v.getEdge(edgeStr)
  if e!=None :
    return e.pointTo
  return None

def pathToEnd(v,paths):
  """寻找v点通过paths这一条路径能到达的终点"""
  end=None
  curV=v
  for path in paths:
    print(curV.val,path)
    curV=edgeToPoint(curV,path)
    if curV==None :
      break
    end=curV
  return end 

def getAllEnds(v,lst):
  """从一个点开始，获取列表里的所有paths所能到达的所有终点和可信概率"""
  ends=[]
  print(v)
  print(lst)
  for item in lst:
    s=item[0]
    end=None  #终点
    # 切分path
    paths=s.split(' ;')
    end=pathToEnd(v,paths)
    if end!=None:
      ends.append([end,item[1]])
    # 可信概率降序排列,从一个点开始也有可能有多条符合情况的路径
    ends=sorted(ends,key=lambda a:a[1],reverse=True)
  return ends





# sents="where does Michael Jordan come from"
# sents="where does Aaron Kemps come from"
# sents="What is Jordan's career?"
# sents="What is Jordan?"
# sents="Who is Jordan?"
# sents="what is US?"
# sents="who was married to Jordan?"

# 就叫“子非”啦，我的机器人哈哈
def askZiFei(sents,g=None):
  # 建立RDF图
  if g==None:
    # 有时间在外面也要用到g，就直接传进来了
    g=getGraph()
  # 从句子中提取三元组
  t=getTriple(sents)
  if not t :
    print('getTriple failed!')
    return None
  arg1,rel,arg2=t
  # 获取实体链接
  arg1Lst=getEntity(arg1)
  arg2Lst=getEntity(arg2)
  # 获取谓词路径
  relLst=getRelPath(rel)

  print('arg1Lst: '+str(arg1Lst))
  print('arg2Lst: '+str(arg2Lst))
  print('relLst: '+str(relLst))

  resourceLst=getResourceLst(arg1Lst,arg2Lst)

  print(resourceLst)

  if len(relLst)==0 :
    print('relLst is null!')
    return None
  # be动词的情况
  if relLst[0][0]=='be':
    # req=requests.get('http://localhost:5001/rdf?v='+arg1Lst[0])
    # print(req.text)
    # data=json.loads(req.text)
    # print(data['name'])
    # 遍历所有的资源，从所有点开始
    ends=[]
    for resStr in resourceLst:
      # 获取所有的path可达终点和可信概率
      if not resStr in g.verteices:
        continue
      v=g.verteices[resStr]
      ends.append([v,0.1])
    
  else:
  
    # 遍历所有的资源，从所有点开始
    ends=[]
    for resStr in resourceLst:
      # 获取所有的path可达终点和可信概率
      if not resStr in g.verteices:
        continue
      v=g.verteices[resStr]
      ends+=getAllEnds(v,relLst)

  print(ends)
  sampleEnds=[(end[0].val,end[1]) for end in ends]
  print(sampleEnds)
  return sampleEnds

# url='http://localhost:5003/rdf?v='+sub+'&e='+pathArr[0][0]
# req = requests.get(url)
# data=json.loads(req.text)
# answer=data['pointTo'].replace('resource/','')
# print(sents)
# print(answer)

