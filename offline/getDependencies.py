# 通过请求'http://nlp.stanford.edu:8080/parser/index.jsp'的接口，调用斯坦福paser来获取句子的依赖关系，后续建立依赖树
import requests
import json
import re
def getDependencies(sents):
  # url='http://nlp.stanford.edu:8080/parser/index.jsp'
  # params = {
  # 'query':sents,
  # 'parserSelect':'English',
  # 'parse':'Parse'
  # }  #python object
  # headers = {
  # }
  # req = requests.post(url, data=params, headers=headers)
  # # print(req.text)
  # result=re.findall(r'<pre class="spacingFree">([\s\S]+?)</pre>',req.text)

  # lst=result[1].split('\n')

  lst=['nsubjpass(married-3, Who-1)', 'auxpass(married-3, was-2)', 'root(ROOT-0, married-3)', 'case(actor-6, to-4)', 'det(actor-6, an-5)', 'nmod:to(married-3, actor-6)', 'nsubj(play-8, actor-6)', 'ref(actor-6, that-7)', 'acl:relcl(actor-6, play-8)', 'case(Philadelphia-10, in-9)', 'nmod:in(play-8, Philadelphia-10)']
  # 过滤掉case开头的依赖，学长说重复了，先不管为啥，做出了再说
  # 我感觉名义主语和关系从句修饰符也重复了，暂时把nsubj也删了吧
  def rmCase(item):
    """过滤case开头的项"""
    return not (item.startswith('case(') ) #or item.startswith('nsubj(')

  print(lst) 
  # ['nsubjpass(married-3, Who-1)', 'auxpass(married-3, was-2)', 'root(ROOT-0, married-3)', 'det(actor-6, an-5)', 'nmod:to(married-3, actor-6)', 'ref(actor-6, that-7)', 'acl:relcl(actor-6, play-8)', 'nmod:in(play-8, Philadelphia-10)']
  lst=list(filter(rmCase,lst))

  return lst



# sents='Who was married to an actor that play in Philadelphia ?'
# sents='Who i love that is girl?'
# print(getDependencies(sents))




