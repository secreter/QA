# 生成RDF图
#
import time
"""
vertex={
val:'resource/!!!',
edges:[]                   #有向边，指向宾语，本节点为主语，边上的val是谓语关系短语
}
edge={
pointTo:v,
val:"name"
}
"""
# 定义点的数据结构
class Vertex:
  def __init__(self,val):
    self.val=val
    self.edges=[]

  # 添加有向边，（从改点指向宾语的边）
  def addEdge(self,e):
    self.edges.append(e)

  def getEdges(self):
    return self.edges

#   定义边的数据结构
class Edge(object):
  def __init__(self,val,pointTo):
    self.val=val
    self.pointTo=pointTo


class Graph(object):
  def __init__(self):
    # 这里用字典，方便查找一个相同val的点是否已经存在图中了
    self.verteices={}
    print('init------------------')

  def addTriple(self,triple):
    # 未添加到verteices里的主语点
    if triple[0] not in self.verteices:
      vSub=Vertex(triple[0])
      self.verteices[triple[0]]=vSub
    else:
      vSub=self.verteices[triple[0]]
    # 未添加到verteices里的宾语点
    if triple[2] not in self.verteices:
      vObj=Vertex(triple[2])
      self.verteices[triple[2]]=vObj
    else:
      vObj = self.verteices[triple[2]]
    #准确来说不会有相同的边，但还是要判断一下
    #这里适合在点的类里判断，但因为本身内存就不够，这里暂时不判断，出问题再说

    e=Edge(triple[1],vObj)   #创建边
    vSub.addEdge(e)          #主语点添加一条有向边

def getGraph():
  # 操作
  g = Graph()
  start = time.time()
  fileLst = ['persondata_en.txt', 'infobox_en_filter.txt']
  # fileLst = ['persondata_en.txt']
  i = 0
  # file=open(r'D:\study\pythonitem\qa\offline\txt\infobox_mini.txt','r',encoding='utf-8')
  for fileName in fileLst:
    file = open(r'D:\study\pythonitem\qa\offline\txt\dist\dbpedia\\' + fileName, 'r', encoding='utf-8')
    line = True
    print('start ' + fileName)
    while line:
      i = i + 1
      line = file.readline()
      if len(line) < 2:
        continue
      # line=line.replace('\n','')
      # print(line)
      try:
        lst = eval(line)
        g.addTriple(lst)
      except SyntaxError:
        print('SyntaxError in eval')
      # print(lst)
      if i % 100000 == 0:
        print(i)
  end = time.time()
  print(end - start)
  print(len(g.verteices))
  return g







