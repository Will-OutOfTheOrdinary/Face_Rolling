from flask import Flask,request,jsonify
import re
import numpy as np
import math
import cv2
from flask_sqlalchemy import SQLAlchemy
from model import app,db,User,ImageFile,TeamBelong,TeamHave
from flask import Blueprint
from sqlalchemy import desc 
team_api = Blueprint('team_app', __name__)

@app.route('/get_team/', methods=['GET'])
def get_team():
    idd=request.args.get("id")
    rec=TeamBelong.query.get(idd)
    if rec is None:
        return jsonify({'status': 404, 'message': '没有'})
    a=[]
    if rec.users is not None:
        for u in rec.users:
            a.append(u.id)
    x={
        "id":idd,
        "number":rec.number,
        "members":a
    }
    return jsonify({'status': 200, 'message': 'success', 'data': x})
    
@app.route('/get_all_team/', methods=['GET'])
def get_all_team():
    ts=TeamBelong.query.order_by(TeamBelong.id)
    a=[]
    for t in ts:
        c=[]
        if t.users is not None:
            for x in t.users:
                c.append(x.id)
        b={
            "id":t.id,
            "name":t.name,
            "members":c
        }
    a.append(b)
    return jsonify({'status': 200, 'message': 'success', 'data': a})
    
@app.route('/search_team/', methods=['GET'])
def search_team():
    search=request.form.get("search")
    recs=TeamBelong.query.filter(TeamBelong.name.ilike("%"+search+"%"  ) if search is not None else "")
    a=[]
    for t in recs:
        c=[]
        if t.users is not None:
            for x in t.users:
                c.append(x.id)
        b={
            "id":t.id,
            "name":t.name,
            "members":c
        }
    a.append(b)
    return jsonify({'status': 200, 'message': 'success', 'data': a})
    
    
@app.route('/get_have_team/', methods=['GET'])
def get_have_team():
    idd=request.args.get("id")
    u=User.query.get(idd)
    recs=u.teamhaves
    a=[]
    for t in recs:
        c=[]
        if t.users is not None:
            for x in t.users:
                c.append(x.id)
        b={
            "id":t.id,
            "name":t.name,
            "members":c
        }
    a.append(b)
    return jsonify({'status': 200, 'message': 'success', 'data': a})
    
@app.route('/get_belong_team/', methods=['GET'])
def get_belong_team():
    idd=request.args.get("id")
    u=User.query.get(idd)
    recs=u.teambelongs
    a=[]
    for t in recs:
        c=[]
        if t.users is not None:
            for x in t.users:
                c.append(x.id)
        b={
            "id":t.id,
            "name":t.name,
            "members":c
        }
    a.append(b)
    return jsonify({'status': 200, 'message': 'success', 'data': a})

@app.route('/add_team_member/', methods=['GET'])
def add_team_member():
    idd1=request.args.get("id_user")
    idd2=request.args.get("id_team")
    t1=TeamBelong.query.get(idd2)
    t2=TeamHave.query.filter(TeamHave.name==t1.name).first()
    u=User.query.get(idd1)
    t1.number=t1.number+1
    t2.number=t2.number+1
    t1.users.append(u)
    u.teambelongs.append(t1)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'success'})
    
@app.route('/delete_team_member/', methods=['GET'])
def delete_team_member():
    idd1=request.args.get("id_user")
    idd2=request.args.get("id_team")
    t1=TeamBelong.query.get(idd2)
    t2=TeamHave.query.filter(TeamHave.name==t1.name).first()
    t1.number=t1.number-1
    t2.number=t2.number-1
    u=User.query.get(idd1)
    t1.users.remove(u)
    u.teambelongs.remove(t1)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'success'})
    
@app.route('/add_have_team/', methods=['GET'])
def add_belong_team():
    idd1=request.args.get("id_user")
    idd2=request.args.get("id_team")
    t=TeamHave.query.get(idd2)
    t.user_id=idd1
    db.session.commit()
    return jsonify({'status': 200, 'message': 'success'})
    
@app.route('/delete_have_team/', methods=['GET'])
def delete_belong_team():
    idd1=request.args.get("id_user")
    idd2=request.args.get("id_team")
    User.query.get(idd1)
    t=TeamHave.query.get(idd2)
    User.teamhaves.remove(t)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'success'})
    
@app.route('/creatTeam/', methods=['POST'])
def creatTeam():
    n=request.args.get("name")
    t1=TeamBelong(name=n,number=0)
    t2=TeamHave(name=n,number=0)
    if TeamHave.query.filter(TeamHave.name==n).first() is not None:
        return jsonify({'status': 404, 'message': 'have exist'})
    db.session.add(t1)
    db.session.add(t2)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'success'})