
from flask import Flask
from flask import request
import json 
f=open(r"./txt/dist/my/relT.txt",'r')
dic=json.load(f)

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/relT', methods=['GET'])
def relT():
  print(request.args)
  rel=request.args.get('rel')
  if rel in dic:
    return json.dumps({rel:dic[rel]})
  return json.dumps({rel:[]})








if __name__ == '__main__':
    app.run(port=5002)