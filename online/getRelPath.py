# 进行图匹配找到答案
from getRelFromN import getTriple
import json
import requests


def getRelPath(rel):
  # 字典里没有is are，先加上，谓词路径设为空，出现的话直接搜索主语，直接返回be
  if rel in ['is','are']:
    return [['be',1]]
  # 根据谓词短语查询到patternid
  fRelT=open('../offline/txt/dist/my/relT.txt','r',encoding='utf-8')
  relT=json.load(fRelT)
  # 根据patternid查询谓词路径path
  fPaths=open('../offline/txt/dist/my/paths_tf-idf.txt','r',encoding='utf-8')
  paths=json.load(fPaths)

  print(rel)

  # print(relT[rel])
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
  return pathArr



