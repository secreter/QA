# 生成谓词路径 
# id '\t\t\t' PS '\t\t\t' m(实体对个数)
from graphGenerate import getGraph
def strToInstance(s):
  """str 还要处理一下，比如Bob smith，处理为resource/Bob_Smith
  """
  s=s.replace(' ','_')
  return 'resource/'+s


def getPath(subVal,objVal):
  """返回从sub到obj的谓词路径，先尝试2个长度的吧"""
  path=[]
  subVal=strToInstance(subVal)
  objVal=strToInstance(objVal)
  global total,notIn
  total=total+2
  if subVal not in g.verteices:
    notIn=notIn+1
    # print(subVal +' not in V')
    return path
  if objVal not in g.verteices:
    notIn=notIn+1
    return path
  sub=g.verteices[subVal]
  obj=g.verteices[objVal]
  stack=sub.edges #sub的所有边
  for edge in stack:
    if edge.pointTo==obj:
      path.append(edge.val)
    else:
      curV=edge.pointTo
      for edgeNext in curV.edges:
        if edgeNext.pointTo==obj:
          path.append(edge.val+' ;'+edgeNext.val)
  return path


g=getGraph()
total=0
notIn=0
file = open(r'D:\study\pythonitem\qa\offline\txt\dist\patty\wikipedia-instances.txt', 'r', encoding='utf-8')
line=True
i=0
with open(r"./txt/dist/my/paths.txt",'w',encoding='utf-8') as dist:
  while line:
    i=i+1
    PS=[]
    line=file.readline()
    lst=line.split('\t\t\t')
    # print(lst)
    pid=lst[0]
    if len(lst)<2:   # make sure lenth enough
      continue
    if len(lst[1])<2:
      continue
    arr=lst[1][:-1].split('\t') #del \n
    # print(arr)
    for pair in arr:
      try:
        pair=eval(pair)
      except SyntaxError:
        print('SyntaxError in eval')
        continue
      # print(pair)
      if len(pair)<2:
        continue
      path=getPath(pair[0],pair[1])
      if len(path)>0:
        PS.append(str(path))
    if len(PS)>0:
      dist.write(pid+'\t\t\t'+'\t'.join(PS)+'\t\t\t'+str(len(arr))+'\n')

    if i%1000==0:
      print(i)
      # break
print(notIn/total)