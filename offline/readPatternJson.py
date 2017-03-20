import json
with open(r"./txt/src/patty/format-patterns.txt",'r',encoding='utf-8') as f:
  # data=f.read()
  dic=json.load(f)


print(dic['987'])
 