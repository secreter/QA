# 给定一个点的val和一个边的val，返回边指向的点的val

from flask import Flask
from flask import request
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
    # 需要从request对象读取表单内容：
    if not request.form['question']:
      return '<h3>没有提问哦！</h3>'
    question=request.form['question']
    # 靠，py的可选参数一定要用等号
    answerLst=askZiFei(question,g=g)
    return '''<form action="/zifei" method="post">
              <p><input name="question" value="'''+question +'''"></p>
              <p><button type="submit">ask zifei</button></p>
              </form>
              <br>
              <h3>'''+str(answerLst)+'''</h3>
              '''

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