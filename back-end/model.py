from flask import Flask,request,jsonify
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import sys
from sqlalchemy.ext.declarative import declarative_base
import configs
app = Flask(__name__)
from sqlalchemy import Table, Column, Integer, ForeignKey

cors = CORS(app)
# 加载配置文件
app.config.from_object(configs)
# db绑定app
db = SQLAlchemy(app)
Base = declarative_base()
    

    
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)  # 设置主键, 默认自增
    name=db.Column(db.String(100))
    password=db.Column(db.String(100))
    phone=db.Column(db.String(100))
    teambelongs = db.relationship("TeamBelong", secondary='User_Goods',back_populates='users')

class ImageFile(db.Model):
    __tablename__ = 'ImageFile'
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(30), index=True)
    path = db.Column(db.String(50))
    user_id = db.Column(db.Integer(),db.ForeignKey('User.id'))
    user = db.relationship('User', backref=db.backref('images'))
    
class TeamBelong(db.Model):
    __tablename__ = 'TeamBelong'
    id = db.Column(db.Integer, primary_key=True)  # 设置主键, 默认自增
    number=db.Column(db.Integer())
    name=db.Column(db.String(100))
    users = db.relationship("User", secondary='User_Goods',back_populates='teambelongs')
    
class TeamHave(db.Model):
    __tablename__ = 'TeamHave'
    id = db.Column(db.Integer, primary_key=True)  # 设置主键, 默认自增
    user_id = db.Column(db.Integer(),db.ForeignKey('User.id'))
    user = db.relationship('User', backref=db.backref('teamhaves'))
    number=db.Column(db.Integer())
    name=db.Column(db.String(100))
    

class User_Goods(db.Model):
    __tablename__ = 'User_Goods'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    TeamBelong_id = db.Column(db.Integer, db.ForeignKey('TeamBelong.id'), nullable=False)

class Course(db.Model):
    _tablename__ = 'Course'
    id = db.Column(db.Integer, primary_key=True)  # 设置主键, 默认自增
    name=db.Column(db.String(100))
    date=db.Column(db.String(100))
    startTime=db.Column(db.String(100))
    endTime=db.Column(db.String(100))
