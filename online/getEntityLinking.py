# 通过dbpedia的接口，获取词语的实体链接，默认返回前5个
import requests
import re
def getEntity(s):
  """返回最多5个实体链接，好像还可以通过参数来配置搜索的类别和返回的个数"""
  url = 'http://lookup.dbpedia.org/api/search.asmx/KeywordSearch'
  param = {
    'QueryString': s
  }
  req = requests.get(url, params=param)
  res = re.findall(r'<Result>[\s\S]+?<Label>(.+?)<\/Label>', req.text)
  return res

print(getEntity('zh'))