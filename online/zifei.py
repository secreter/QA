# 给定一个点的val和一个边的val，返回边指向的点的val

from flask import Flask
from flask import request
import time
import json
import sys
sys.path.append("../offline")
from graphGenerate import getGraph
from matchGraph import askZiFei


app = Flask(__name__)
g=getGraph()
@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/zifei', methods=['GET'])
def signin_form():
    return '''<form action="/zifei" method="post">
              <p><input name="question"></p>
              <p><button type="submit">ask zifei</button></p>
              </form>'''

@app.route('/zifei', methods=['POST'])
def signin():
    start = time.clock()
    # 需要从request对象读取表单内容：
    if not request.form['question']:
      return '<h3>没有提问哦！</h3>'
    question=request.form['question']
    # 靠，py的可选参数一定要用等号
    answerLst=askZiFei(question,g=g)
    if not answerLst:
      return '''
              
              <form center action="/zifei" method="post">
              <p><input style="width:400px;height:60px" name="question" value="'''+question +'''"></p>
              <p><button type="submit">ask</button></p>
              </form>
              <br>
              <h3>数据集中没有答案，子非也没办法哦~换个问题问问吧</h3>
              '''
    elapsed = (time.clock() - start)
    return '''
              <form center action="/zifei" method="post">
              <p><input style="width:400px;height:60px" name="question" value="'''+question +'''"></p>
              <p><button type="submit">ask</button></p>
              </form>
              <br>
              花费时间：'''+str(elapsed)+'''s
              <br>
              '''+str(['<h3><p>答案：'+item[0].split('/')[1]+'      得分：'+str(item[1])+'</p><p>维基主页：https://en.wikipedia.org/wiki/'+item[0].split('/')[1]+'</p></h3>' for item in answerLst if len(item[0].split('/'))>1])[1:-1].replace("'",'')

@app.route('/get_zifei', methods=['GET'])
def get_zifei():
    start = time.clock()
    question=request.args.get('question')
    # 需要从request对象读取表单内容：
    if not question:
      return json.dumps({
        'error':1,
        'msg':'question is null'
        })


    # 靠，py的可选参数一定要用等号
    answerLst=askZiFei(question,g=g)
    elapsed = (time.clock() - start)
    if not answerLst:
      return json.dumps({
        'error':2,
        'time':str(elapsed)+'s',
        'msg':'这个问题数据集没有答案，换个问题试试吧~'
        })
    item=answerLst[0]
    return json.dumps({
        'error':0,
        'time':str(elapsed)+'s',
        'msg':'success',
        'answer':item[0].split('/')[1],
        'score':item[1],
        'wiki':'https://en.wikipedia.org/wiki/'+item[0].split('/')[1]
        })



@app.route('/edge', methods=['GET'])
def edge():

    print(request.args)
    v=request.args.get('v')
    v='resource/'+v.replace(' ','_')
    if v in g.verteices:
      res={
      "name":g.verteices[v].val,
      "edges":[edge.val for edge in g.verteices[v].edges]
      }
      return json.dumps(res)
    else:
      return 'no this vertex!'             

@app.route('/rdf', methods=['GET'])
def rdf():
    print(request.args)
    v=request.args.get('v')
    if not v:
      return json.dumps({"error":"arg v is empty!"})
    v='resource/'+v.replace(' ','_')
    e=request.args.get('e')
    if not e:
      return json.dumps({"error":"arg e is empty!"})
    if v in g.verteices:
      for edge in g.verteices[v].edges:
        if edge.val==e:
          res={
          "name":g.verteices[v].val,
          "edge":e,
          "pointTo":edge.pointTo.val,
          "edges":[eg.val for eg in g.verteices[v].edges],
          "error":''
          }
          return json.dumps(res)
      return json.dumps({"error":"no such edge!"})
    else:
      return json.dumps({"error":"no such vertex!"})




if __name__ == '__main__':
    app.run(port=5004)