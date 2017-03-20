# 调用getDependencies()来获取问题N的关系依赖，然后构建依赖树Y，再从Y中提取关系短语rel
# 最后提取三元组[rel,arg1,arg2].注意，一个问题里面可能包含多个三元组
import getDependencies
import re
# sents='Who was married to an actor that play in Philadelphia ?'
# sents='I love a girl who\' name is buzhidao ?'
sents='Marry\'s gender is male ?'

deLst=getDependencies.getDependencies(sents)
print(deLst)

def getSpecifyDependencies(nodeStr,deLst):
  """"获取指定的以nodeStr为(start,end)start的所有依赖，返回一个list，
  这里的nodeStr包含-index，因为可能存在同名的单词
  其实还可以返回deLst除去结果剩下的新deLst，但是这样有点不太美观，句子不长
  不影响性能，先这样"""
  lstGe=filter(lambda s:s.find('('+nodeStr+',')>-1, deLst)
  return list(lstGe)

def initNode(nodeStr):
  """初始化应该node"""
  lst=nodeStr.split('-')
  node={
    'index':lst[1],
    'val':lst[0],
    'nodeStr':nodeStr,
    'children':[],
    'parent':[]
  }
  return node

def traversal(node,callback=''):
  """遍历树"""
  
  if callback:
    callback(node)
  else:
    print(node['val'])
    if len(node['parent'])>0:
      print('--parent:'+node['parent'][0]['val'])
  for child in node['children']:
    traversal(child)

def findNode(node,nodeStr):
  """返回指定nodeStr的node"""
  if node['nodeStr']==nodeStr:
    return node
  for child in node['children']:
    temp=findNode(child,nodeStr)
    if (temp != None):
      return temp
  return None

def getDependencyTree(deLst):
  """这里采用一个栈来构建依赖树，从root节点开始root(start,end)
  读取start，end，记录一条表start指向end，然后root(start,end)
  出栈，所有以end为起始点的依赖入栈，若没有以end为起始点的依赖，就
  再pop一个依赖，直到栈为空"""
  stack=[]
  appearedDict={}  #记录出现过的nodeStr，因为我发现有时候依赖里面会出现环，我决定在深度遍历过程中，对指向父节点的衣领删除
  root={
    'index':0,
    'nodeStr':'ROOT-0',
    'val':'ROOT',
    'children':[],
    'parent':[]  #不知道会不会出现多个父亲的节点，应该不会
  }
  # 获取root节点的指定lst
  speLst=getSpecifyDependencies('ROOT-0',deLst)
  stack=stack+speLst
  crossStack=[root]

  # 当前节点初始化为root
  curNode=root
  while len(stack)>0:
    # 获取依赖字符串'nmod:to(married-3, actor-6)'
    deStr=stack.pop()
    # 匹配出结束节点的nodestr,,,'married-3'
    nodeStr=re.findall(r', (.+)\)',deStr)[0]
    # y有时候会出现环，这里我不允许child节点的孩子指向它父亲，直接忽略
    if nodeStr not in appearedDict:
      appearedDict[nodeStr]=True
    else:
      print(nodeStr+'=====had appeared')
      continue
    newNode=initNode(nodeStr)
    # 获取前缀，如果是类似nmod:in这样的，就增加应该in节点在start和end之间
    prefix=re.findall(r'(.*)\(',deStr)[0]
    if prefix.startswith('nmod:'):
      # 因为初始化node的时候没有index，先随便加一个
      insertNodeStr=prefix[5:]+'-None'
      insertNode=initNode(insertNodeStr)
      curNode['children'].append(insertNode)
      insertNode['parent'].append(curNode)
      curNode=insertNode


    # print(nodeStr)
    curNode['children'].append(newNode)
    newNode['parent'].append(curNode)
    curNode=newNode

    speLst=getSpecifyDependencies(nodeStr,deLst)
    if len(speLst)==0 and len(stack)>0:
      # speLst不为空，说明往stack里又增加了一个分叉口，树的高度增加1
      # 这里我们要记住分叉时的父节点，因为等这条支路走到头要返到最近的
      # 分叉节点
      deStr=stack[-1] 
      nodeStr=re.findall(r'\((.*),',deStr)[0]
      print(nodeStr)
      curNode=findNode(root,nodeStr)
      print(curNode)
    stack=stack+speLst
    print(stack)
  return root


root=getDependencyTree(deLst)
# print(root)
print('-------------------')
traversal(root)