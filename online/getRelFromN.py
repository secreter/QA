# 调用getDependencies()来获取问题N的关系依赖，然后构建依赖树Y，再从Y中提取关系短语rel
# 最后提取三元组[rel,arg1,arg2].注意，一个问题里面可能包含多个三元组
import getDependencies
import re
import json
f=open(r"../offline/txt/dist/my/relT.txt",'r')
relT=json.load(f)
relArr=[] #存储获取的关系短语
# dicW={
#   # 'was married to':['was','married']
# } #rel[w]，如论文中所讲用来记录指定的关系短语在哪些节点中出现过
# sents='Who was married to an actor that play in Philadelphia ?'
# # sents='I love a girl who\' name is buzhidao ?'
# sents="What is Jordan's career?"
# # sents="what is the tallest building in China"
# # sents="where does Aaron Kemps come from"




def getSpecifyDependencies(nodeStr,deLst):
  """"获取指定的以nodeStr为(start,end)start的所有依赖，返回一个list，
  这里的nodeStr包含-index，因为可能存在同名的单词
  其实还可以返回deLst除去结果剩下的新deLst，但是这样有点不太美观，句子不长
  不影响性能，先这样"""
  lstGe=filter(lambda s:s.find('('+nodeStr+',')>-1, deLst)
  return list(lstGe)
def initEdge(edgeStr,edge2Str):
  """记录边上的关系和边指向的节点的nodeStr,虽然这里结构惨不忍睹，第一次写py，现在改改动比较大"""
  edge={
    'val':edgeStr,
    'edge2Str':edge2Str  #所指向
  }
  return edge

def initNode(nodeStr):
  """初始化应该node"""
  lst=nodeStr.split('-')
  node={
    'index':lst[1],
    'val':lst[0],
    'nodeStr':nodeStr,
    'children':[],
    'parent':[],
    'p2cEdges':[],
    'c2pEdges':[],
    'belong2Y':False
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
      kids="--kids:"
      for child in node['children']:
        kids+=child['val']+"、"
      print(kids)
      p2cS="--p2cEdges:"
      for edge in node['p2cEdges']:
        p2cS+='('+edge['val']+','+edge['edge2Str']+")、"
      print(p2cS)
      c2pS="--c2pEdges:"
      for edge in node['c2pEdges']:
        c2pS+=edge['val']+"、"
      print(c2pS)
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
    'parent':[],  #不知道会不会出现多个父亲的节点，应该不会
    'p2cEdges':[], #父亲到孩子的节点
    'c2pEdges':[],
    'belong2Y': False
  }
  # 获取root节点的指定lst,就是包含ROOT-0的项
  speLst=getSpecifyDependencies('ROOT-0',deLst)
  print('speLst---')
  print(speLst)
  stack=stack+speLst
  crossStack=[root]

  # 当前节点初始化为root
  curNode=root
  while len(stack)>0:
    # 获取依赖字符串'nmod:to(married-3, actor-6)'
    deStr=stack.pop()
    #'nmod:to(married-3, actor-6)' 依次是 edgeStr，pNodeStr，nodeStr
    #获取父节点的pNodeStr
    pNodeStr = re.findall(r'\((.+),', deStr)[0]
    edgeStr = re.findall(r'(.*)\(', deStr)[0]
    # 匹配出结束节点的nodestr,,,'married-3'
    nodeStr=re.findall(r', (.+)\)',deStr)[0]
    # y有时候会出现环，这里我不允许child节点的孩子指向它父亲，直接忽略
    if nodeStr not in appearedDict:
      appearedDict[nodeStr]=True
    else:
      print(nodeStr+'=====had appeared')
      continue
    newNode=initNode(nodeStr)  #Tokyo-6
    p2cEdge=initEdge(edgeStr,nodeStr)  #nmod:of
    c2pEdge=initEdge(edgeStr,pNodeStr) #child 到 parent 的边
    # 获取前缀，如果是类似nmod:in这样的，就增加应该in节点在start和end之间
    prefix=re.findall(r'(.*)\(',deStr)[0]
    if prefix.startswith('nmod:'):
      # 因为初始化node的时候没有index，先随便加一个
      insertNodeStr=prefix[5:]+'-None'
      insertNode=initNode(insertNodeStr)  #of-None
      curNode['children'].append(insertNode)
      # 加上的边暂时用nmod和obj来表示
      c2pEdge = initEdge('nmod', insertNodeStr)
      p2cEdge = initEdge('obj', nodeStr)
      insertNode['c2pEdges'].append(c2pEdge)
      curNode['p2cEdges'].append(c2pEdge)
      print(nodeStr+',,,,,,,,,,,,,'+edgeStr)
      print(curNode['nodeStr'])
      insertNode['parent'].append(curNode)
      curNode=insertNode


    # print(nodeStr)
    curNode['children'].append(newNode)
    curNode['p2cEdges'].append(p2cEdge)
    newNode['parent'].append(curNode)
    newNode['c2pEdges'].append(c2pEdge) #p2cEdge
    curNode=newNode

    speLst=getSpecifyDependencies(nodeStr,deLst)
    print('speLst---')
    print(speLst)
    if len(speLst)==0 and len(stack)>0:
      # speLst不为空，说明往stack里又增加了一个分叉口，树的高度增加1
      # 这里我们要记住分叉时的父节点，因为等这条支路走到头要返到最近的
      # 分叉节点
      deStr=stack[-1] 
      nodeStr=re.findall(r'\((.*),',deStr)[0]
      # print(nodeStr)
      curNode=findNode(root,nodeStr)
      # print(curNode)
    stack=stack+speLst
    # print(stack)
  return root['children'][0] # 不要ROOT这个虚拟节点了

def addPL(root):
  """PL是一个list,每个节点包含一个val，PL就是relT中所有包含val的关系短语
  集合，加到每一个节点上作为属性"""
  root['PL']=[]  #发现be动词是找不到的，这里默认加上,（还是加到字典末尾吧
  for rel in relT:

    relArr=rel.split(' ') # 是短语的话用空格切成单个单词的数组
    if root['val'] in relArr:
      # if rel == "was married to":
      #   print(rel + "!!!in " + root['val'])
      root['PL'].append(rel)
      # print(child['val']+' in '+rel) 
  for child in root['children']:
    addPL(child)

  return root
# 探测
def probe(node,PL,dicW):
  for child in node['children']:
    intersectionPL=list(set(PL)&(set(child['PL'])))  #交集
    if len(intersectionPL)==0:  #交集为空返回
      return
    else:
      # 上一级dicw的有些key因为已经不在intersectionPL里了，所以我们要删除他们
      oldKeys=list(dicW.keys())  #没删除之前的
      dropKeys=set(oldKeys)-set(intersectionPL)  #要删除的
      # if node['val']=='play':
      #   print(intersectionPL)
      # for dropKey in dropKeys:
        # dicW[dropKey]=[]  #这里置空，删除后面检查的时候还会遍历到
      for rel in intersectionPL:
        if rel not in dicW:
          dicW[rel]=[]
        # dicW[rel].append(child['val']) #表示在这个节点出现过
        dicW[rel].append(child['nodeStr']) #表示在这个节点出现过
      probe(child,intersectionPL,dicW)

# 获取关系嵌入
def getRel(root):
  PL=root['PL']
  dicW={}
  #初始化记录节点是否出现过的字典
  for rel in PL:
    if rel not in dicW:
      dicW[rel]=[]
    # dicW[rel].append(root['val'])
    dicW[rel].append(root['nodeStr'])
  #探测以root为根的所有子节点，在dicw中标记出出现过的单词
  probe(root,PL,dicW)
  #遍历PL，查看是否存在rel，rel的每个单词都在子树中出现过
  for rel in PL:
    # rel 中所有单词都在子树上出现过
    # 元素一样但出现的顺序不一定一样，所以是集合的比较
    # if set(['was','married','to'])<=set(rel.split(' ')):
    #   print(set(rel.split(' ')))
    #   print(set(dicW[rel]))
    #   过滤掉[[]]的str
    # if set(filter(lambda s:not s.startswith('[['),rel.split(' ')))==set(dicW[rel]): #暂时注释掉
    if set( rel.split(' ')) == set(map(lambda s:s.split('-')[0],dicW[rel])):
      global  relArr  #全局记录所有满足条件的关系短语
      relArr.append((rel,root,dicW[rel]))
  #深度优先对所有子节点进行查找是否存在以它为根的关系短语
  for child in root['children']:
    getRel(child)

def markSubTreeY(root,lstY):
  """关系短语找到之后，我们需要找到包涵这些节点的子树，这里我们用belong2Y来标记出来"""
  if root['nodeStr'] in lstY:
    root['belong2Y'] = True
  for child in root['children']:
    markSubTreeY(child,lstY)

#寻找node下的复合关系
def findCompound(node):
  """比如姓名Aaron Kemps就是一个复合关系，但是当我们找主语或宾语的时候，只会找到Kemps，
  所以我决定顺着这个节点在找一下有没有复合关系，就观察而言，找到的复合关系应该返回反转后
  的串，例如名字应该是搜索到Kemps和Aaron节点，这里就只搜索一级好了"""
  s=node['val']
  for edge in node['p2cEdges']:
    if edge['val']=='compound':
      s=edge['edge2Str'].split("-")[0]+' '+s
      return s
  return s

# 从这个关系短语的根节点开始向下寻找主语
def findSub(root):
  #不是关系子树
  if root['belong2Y'] ==False:
    return
  subFlagArr=['subj','nsubj', 'nsubjpass', 'csubj', 'csubjpass', 'xsubj', 'poss']
  stack=[root]
  while stack:
    cur=stack.pop()
    for edge in cur['p2cEdges']:
      #边上的关系属于特征关系
      if edge['val'] in subFlagArr:
        subNode=findNode(cur,edge['edge2Str'])
        #保证他不属于关系短语
        if subNode['belong2Y']==False:
          return findCompound(subNode)
    stack+=cur['children']
  return None

# 从这个关系短语的根节点开始向下寻找宾语
def findObj(root):
  #不是关系子树
  if root['belong2Y'] ==False:
    return
  objFlagArr=['obj','pobj', 'dobj', 'iobj']
  stack=[root]
  while stack:
    cur=stack.pop()
    print('findObj --stack pop v:'+cur['val'])
    for edge in cur['p2cEdges']:
      print('findObj --stack pop v edge p2cEdges:'+edge['val'])
      #边上的关系属于特征关系
      if edge['val'] in objFlagArr:
        objNode=findNode(cur,edge['edge2Str'])
        #保证他不属于关系短语
        if objNode['belong2Y']==False:
          return findCompound(objNode)
    stack+=cur['children']
  return None

# 寻找疑问词
def findQuestionWord(node):
  """当主语或宾语有一个为空的时候，找node下的最近的疑问词返回"""
  whArr=['when','where','why','who','which','what','how']
  # 维护一个队列来实现宽度优先遍历
  queue=[node]
  # 后补的，处理根节点是wh
  if node['val'].lower() in whArr:
    return node['val']
  while queue:
    cur=queue.pop()
    for child in cur['children']:
      if child['belong2Y']==False and child['val'] in whArr:
        return child['val']
    queue=cur['children']+queue #加再前面，宽度优先遍历
  return None

def readData(func):
  """装饰器，只读一遍文件"""
  # 根据谓词短语查询到patternid
  fRelT=open('../offline/txt/dist/my/relT.txt','r',encoding='utf-8')
  relT=json.load(fRelT)
  # 根据patternid查询谓词路径path
  fPaths=open('../offline/txt/dist/my/paths_tf-idf.txt','r',encoding='utf-8')
  paths=json.load(fPaths)
  def wrap(*args,**kwargs):
    return func(relT,paths,*args,**kwargs)
  return wrap

#另一个文件里的，循环引用了，拿过来
@readData
def getRelPath(relT,paths,rel):
  # 字典里没有is are，先加上，谓词路径设为空，出现的话直接搜索主语，直接返回be
  if rel in ['is','are']:
    return [['be',1]]
  # # 根据谓词短语查询到patternid
  # fRelT=open('../offline/txt/dist/my/relT.txt','r',encoding='utf-8')
  # relT=json.load(fRelT)
  # # 根据patternid查询谓词路径path
  # fPaths=open('../offline/txt/dist/my/paths_tf-idf.txt','r',encoding='utf-8')
  # paths=json.load(fPaths)

  # print(rel)

  # print(relT[rel])
  # 多个数组合并
  pathArr=[]
  for pid in relT[rel]:
    if pid in paths:
      pathArr+=paths[pid]

  if len(pathArr)>5:
    # 排序并取top-3
    pathArr=sorted(pathArr,key=(lambda x:x[1]), reverse=True)[:5]
  else:
    pathArr=sorted(pathArr,key=(lambda x:x[1]), reverse=True)

  print(pathArr)
  return pathArr



# 这里用全局
def getTriple(sents):

  """获取问题里的三元组，不一定只有一个，比如复合语句里就会有多个
  但还是那样，这我只分析简单到只有一个的情况，没时间写论文了"""
  global relArr 
  relArr=[] #先置空，不然每次调用的是追加
  deLst = getDependencies.getDependencies(sents)
  print(deLst)
  #获取依赖树
  root=getDependencyTree(deLst)
  # print(root)
  print(root['children'])
  print('-------------------')
  #遍历看看
  traversal(root)
  #给每个节点添加候选关系短语
  root=addPL(root)
  #抽取关系短语，是一个数组，记录在全局变量relArr里，（rel,node）
  getRel(root)  #提取关系短语
  
  relArr=sorted(relArr,key=lambda a:len(a[0]),reverse=True)  #排序，选择关系短语最长的一个
  print([item[0] for item in relArr])
  if len(relArr)>0:
    #暂时就默认第一个就是正确结果，但其实不一定，有很多情况，所以只有简单的句子能成功，最好恰好提取的只有一个关系短语
    tu = relArr[0] #（rel,root,lstY）
    # print(tu)
    print(tu[0])
    print(tu[1]['val'])
    print(tu[2])
  else:
    # 我发现 is，are 也是找不到的，这里如果没找到关系短语，把is，are算上

    print('not find rel phrase!')
    return None

  def findTriple(tu):
    # 把包含关系词的子树标记出来
    relRoot=tu[1]
    markSubTreeY(relRoot, tu[2])
    #寻找主语
    subStr=findSub(relRoot)
    # 寻找宾语
    objStr = findObj(relRoot)
    # print('objstr:'+objStr)
    if subStr==None:
      # 规则3：如果t根节点的父节点和它的子节点有类主语关系，添加子节点到arg1中。
      relRoot['parent'][0]['belong2Y']=True #因为前面代码的原因，不是关系子树就直接返回了，这里算它是吧
      subStr = findSub(relRoot['parent'][0])
      relRoot['parent'][0]['belong2Y'] = False
      if subStr == None:
        subStr=findQuestionWord(root)
        # 找不到疑问词就返回吧
        if subStr==None:
          print('sub is none')
        # return None
    if objStr==None:
      objStr=findQuestionWord(relRoot)
      if objStr==None:
        # 从整棵树的根找一次
        objStr = findQuestionWord(root)
        if objStr == None:
          print('obj is none')
        # return None
    # 两个都为空就没得玩了，直接返回
    if subStr == None or objStr == None:
      print('sub or obj are none')
      return None
    print((subStr,tu[0],objStr))
    return (subStr,tu[0],objStr)

  #尝试tu = relArr[0]
  for tu in relArr:
    print('!!')
    print(tu[1]['val'])
    t=findTriple(tu)
    #(who,is,who),重新尝试下一个rel
    if t==None or t[0]==t[2] or len(getRelPath(t[1]))==0:
      # print('tu:'+t[0]+'__'+t[2]+'--'+len(relArr))
      continue
      # 获取谓词路径,本来下一环节才获取的，但是有时候
      # 存在获取不到的时候，这个时候可以换一个试试，提高点
      # 召回率，将就下啦，毕业要紧
      # rel=tu[1]
    else:
      return t
# sents="What is Jordan's career?"
# # sents="What is Jordan?"
# # sents="Where is Jordan?"
# # sents="What is Jordan?"
# sents="where does Aaron Kemps come from"
# # sents='Who was married to an actor that play in Philadelphia ?'
# sents="who was married to Jordan?"
# sents="what is the population of Tokyo?"
# sents=" What is the birth place of Abraham Lincoln??"
# t=getTriple(sents)
# print(t)