from flask import Flask,request,jsonify
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import sys
import configs
app = Flask(__name__)


cors = CORS(app)
# 加载配置文件
app.config.from_object(configs)
# db绑定app
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)  # 设置主键, 默认自增
    name=db.Column(db.String(100))
    password=db.Column(db.String(100))
    
class ImageFile(db.Model):
    __tablename__ = 'ImageFile'
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(30), index=True)
    path = db.Column(db.String(50), index=True)