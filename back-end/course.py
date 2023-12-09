from flask import Flask,request,jsonify
import re
import numpy as np
import math
from flask_sqlalchemy import SQLAlchemy
from model import app,db,User,Course
from flask import Blueprint
course_api = Blueprint('course_app', __name__)

@app.route('/addCourse',methods=['POST'])
def addCourse():
    teamName = request.form.get("teamName")
    c = Course.query.filter(Course.name==teamName).first()
    if c is None:
        return jsonify({'status': 400, 'message': '已存在', 'data': ''})
    new_course=Course(name=teamName)
    db.session.add(new_course)
    db.session.commit()
    use={
    'id':new_course.id,
    'teamName' : teamName,
    }
    return jsonify({'status': 201, 'message': 'success', 'data': use})
    
@app.route('/searchCourse',methods=['POST'])
def searchCourse():
    keyWord=request.form.get("keyWord")
    c = Course.query.filter(Course.name.ilike("%"+keyWord+"%"  ) if keyWord is not None else "",).first()
    use={
    'id':c.id,
    'teamName' : c.name,
    }
    return jsonify({'status': 201, 'message': 'success', 'data': use})

@app.route('/getCourseInfor',methods=['POST'])
def getCourseInfor():
    courseName=request.form.get("courseName")
    c = Course.query.filter(Course.name==courseName).first()
    use={
    'id':c.id,
    'teamName' : c.name,
    }
    return jsonify({'status': 201, 'message': 'success', 'data': use})