
from model import app,db
from user import user_api
from  geventwebsocket.websocket import WebSocket,WebSocketError
from  geventwebsocket.handler import WebSocketHandler
from  gevent.pywsgi import WSGIServer
from face import face_api
from team import team_api
from communicaty import communicaty_api
from course import course_api
app.register_blueprint(user_api)
app.register_blueprint(face_api)
app.register_blueprint(team_api)
app.register_blueprint(communicaty_api)
app.register_blueprint(course_api)
if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        #db.create_all()
        app.run(host="0.0.0.0", port=443, debug=True)
        http_serve=WSGIServer(("0.0.0.0",8001),app,handler_class=WebSocketHandler)
        http_serve.serve_forever()
