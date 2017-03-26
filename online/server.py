# import socket

# HOST, PORT = '', 8888

# listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# listen_socket.bind((HOST, PORT))
# listen_socket.listen(1)
# print('Serving HTTP on port %s ...' % PORT)
# while True:
#     client_connection, client_address = listen_socket.accept()
#     request = client_connection.recv(1024)
#     print(request)

#     http_response = b"""
# HTTP/1.1 200 OK

# Hello, World!
# """
#     client_connection.sendall(http_response)
#     client_connection.close()


from flask import Flask
from flask import request
from graphGenerate import getGraph
import json 


app = Flask(__name__)
g=getGraph()
@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

@app.route('/rdf', methods=['GET'])
def rdf():
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




if __name__ == '__main__':
    app.run(port=5001)