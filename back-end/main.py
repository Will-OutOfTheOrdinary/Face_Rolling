from model import app,db
from user import user_api
from face import face_api
from team import team_api
app.register_blueprint(user_api)
app.register_blueprint(face_api)
app.register_blueprint(team_api)
if __name__ == '__main__':
    db.create_all()
    app.run(host="0.0.0.0", port=443, debug=True)
