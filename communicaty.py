
from flask import  Flask ,request,render_template
from  geventwebsocket.websocket import WebSocket,WebSocketError
from  geventwebsocket.handler import WebSocketHandler
from  gevent.pywsgi import WSGIServer
from model import app,db
from flask import Blueprint

from main import user_socket_dict1,user_socket_dict2
import json
communicaty_api = Blueprint('communicaty_app', __name__)

@app.route('/index/')
def index():
    return render_template('websocket.html')

# user_socket_list = []
user_socket_dict={}

@app.route('/chat_room/<username>')
def ws(username):
    user_socket=request.environ.get("wsgi.websocket")
    if not user_socket:
        return "请以WEBSOCKET方式连接"

    user_socket_dict1[username]=user_socket
    print(user_socket_dict1)

    while True:
        try:
            user_msg = user_socket.receive()
            for user_name,u_socket in user_socket_dict1.items():

                who_send_msg={
                    "send_user":username,
                    "send_msg":user_msg
                }

                if user_socket == u_socket:
                    continue
                u_socket.send(json.dumps(who_send_msg))

        except WebSocketError as e:
            user_socket_dict1.pop(username)
            print(user_socket_dict1)
            print(e)



@app.route('/chat/<username>')
def ws(username):
    user_socket=request.environ.get("wsgi.websocket")
    if not user_socket:
        return "请以WEBSOCKET方式连接"

    user_socket_dict2[username]=user_socket
    print(user_socket_dict2)

    while True:
        try:
            user_msg = user_socket.receive()
            user_msg=json.loads(user_msg)
            to_user_socket = user_socket_dict2.get(user_msg.get("to_user"))
            send_msg={
                "send_msg":user_msg.get("send_msg"),
                "send_user":username
            }
            to_user_socket.send(json.dumps(send_msg))
        except WebSocketError as e:
            user_socket_dict2.pop(username)
            print(user_socket_dict2)
            print(e)