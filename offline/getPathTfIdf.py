# 从path_tf读取数据，计算idf，然后计算tf-idf，再降序排列
# ' ;'连接的是谓词路径
import math
import json
def isIn2DArr(s,arr):
  """s是否出现在二维数组中过
  但这里只是二维数组的第0个有用"""
  for lst in arr:
    if s==lst[0]:
      return True
  return False
def getShowTimes(s):
  """获取s在dic多少数组中出现过"""
  count=0
  for key in dic:
    if isIn2DArr(s,dic[key]):
      count=count+1
  return count


file = open(r'./txt/dist/my/paths_tf.txt', 'r', encoding='utf-8')
line=True
i=0
dic={}
with open(r"./txt/dist/my/paths_tf—idf.txt",'w',encoding='utf-8') as dist:
  while line:
    line=file.readline()

    if line=='\n' or line=='':
      continue
    lst=line[:-1].split('\t\t\t')
    # print(lst)
    if lst[0] not in dic:
      arr=eval(lst[1])
      arr=list(map(lambda s:eval(s),arr))
      dic[lst[0]]=arr

    # print(line)
    # print(lst)
    # print(dic)
    # break
  print('while end')
  # pattern 的总数
  countT=len(dic)
  print(countT)
  for key in dic:
    pathArr=dic[key]
    for lst in pathArr:
      i+=1
      #['producer', 0.01492537],path ,tf
      times=getShowTimes(lst[0])
      idf=round(math.log(countT/(times+1)),8)
      # lst.append(idf)
      confidence=round(lst[1]*idf,8)
      # 查看异常
      if abs(confidence-0)<0.00000001:
        print(lst[0])
        print(confidence)
      # lst.append(confidence)
      lst[1]=confidence
      if i%100==0:
        print(i)
    # 排序
    dic[key]=sorted(pathArr,key=(lambda x:x[1]), reverse=True)
  # print(dic)
  json.dump(dic,dist)

