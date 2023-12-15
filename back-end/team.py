from flask import Flask,request,jsonify
import re
import numpy as np
import math
import cv2
import ast
import xlrd
from flask_sqlalchemy import SQLAlchemy
from model import app,db,User,ImageFile,TeamBelong,TeamHave,User_Goods
from flask import Blueprint
from sqlalchemy import desc 
team_api = Blueprint('team_app', __name__)

@app.route('/getTeamInfo', methods=['POST'])
def getTeamInfo():
    idd=request.form.get("id")
    rec=TeamBelong.query.get(idd)
    if rec is None:
        xx={
        "id":idd,
        "number":-1,
        "members":[]
        }
        return jsonify({'status': 404, 'message': '没有','data':xx})
    a=[]
    if rec.users is not None:
        for u in rec.users:
            siji={
                'id':u.id,
                'name':u.name,
                'phone':u.phone,
                'password':u.password
            }
            a.append(siji)
    x={
        "id":idd,
        "number":rec.number,
        "members":a
    }
    return jsonify({'status': 200, 'message': 'success', 'data': x})
    
@app.route('/get_all_team', methods=['GET'])
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
    
@app.route('/searchTeam', methods=['POST'])
def searchTeam():
    search=request.form.get("teamName")
    recs=TeamBelong.query.filter(TeamBelong.name.ilike("%"+search+"%"  ) if search is not None else "")
    a=[]
    for t in recs:
        c=[]
        if t.users is not None:
            for x in t.users:
                c.append(x.id)
        b={
            "id":t.id,
            "teamname":t.name,
            "members":c
        }
    a.append(b)
    return jsonify({'status': 200, 'message': 'success', 'data': a})
    
    
@app.route('/get_have_team', methods=['GET'])
def get_have_team():
    idd=request.form.get("id")
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
    
@app.route('/get_belong_team', methods=['GET'])
def get_belong_team():
    idd=request.form.get("id")
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

@app.route('/add_team_member', methods=['GET'])
def add_team_member():
    idd1=request.form.get("id_user")
    idd2=request.form.get("id_team")
    t1=TeamBelong.query.get(idd2)
    t2=TeamHave.query.filter(TeamHave.name==t1.name).first()
    u=User.query.get(idd1)
    t1.number=t1.number+1
    t2.number=t2.number+1
    t1.users.append(u)
    u.teambelongs.append(t1)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'success'})
    
@app.route('/delete_team_member', methods=['GET'])
def delete_team_member():
    idd1=request.form.get("id_user")
    idd2=request.form.get("id_team")
    t1=TeamBelong.query.get(idd2)
    t2=TeamHave.query.filter(TeamHave.name==t1.name).first()
    t1.number=t1.number-1
    t2.number=t2.number-1
    u=User.query.get(idd1)
    t1.users.remove(u)
    u.teambelongs.remove(t1)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'success'})
    
@app.route('/add_have_team', methods=['GET'])
def add_belong_team():
    idd1=request.form.get("id_user")
    idd2=request.form.get("id_team")
    t=TeamHave.query.get(idd2)
    t.user_id=idd1
    db.session.commit()
    return jsonify({'status': 200, 'message': 'success'})
    
@app.route('/delete_have_team', methods=['GET'])
def delete_belong_team():
    idd1=request.form.get("id_user")
    idd2=request.form.get("id_team")
    User.query.get(idd1)
    t=TeamHave.query.get(idd2)
    User.teamhaves.remove(t)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'success'})
    
@app.route('/creatTeam', methods=['POST'])
def creatTeam():
    n=request.form.get("teamName")
    teammate=request.form.get("teammate")
    res = ast.literal_eval(teammate)
    if TeamHave.query.filter(TeamHave.name==n).first() is None:
        t1=TeamBelong(name=n,number=0)
        t2=TeamHave(name=n,number=0)
        db.session.add(t1)
        db.session.add(t2)
        db.session.commit()
    else:
        t1=TeamBelong.query.filter(TeamBelong.name==n).first()
    #if TeamHave.query.filter(TeamHave.name==n).first() is not None:
    #    return jsonify({'status': 404, 'message': 'have exist'})
    t1.number=len(res)
    db.session.commit()
    for idd in res:
        if User_Goods.query.filter(User_Goods.user_id==idd,User_Goods.TeamBelong_id==t1.id).first() is not None:
            continue
        ug=User_Goods()
        ug.user_id = t1.id
        ug.TeamBelong_id = idd
        db.session.add(ug)
        db.session.commit()
    return jsonify({'status': 200, 'message': 'success','data':{'id':t1.id}})

@app.route('/creatTeamByFile', methods=['POST'])
def creatTeamByFile():
    #n=request.form.get("teamName")
    file=request.files.get("file")
    f = file.read()
    clinic_file = xlrd.open_workbook(file_contents=f)
        # sheet1
    table = clinic_file.sheet_by_index(0)
    nrows = table.nrows
    n=table.row_values(0)[0]
    print(n)
    print("\n\n\n\n")
    if TeamBelong.query.filter(TeamBelong.name==n).first() is None:
        t1=TeamBelong(name=n,number=0)
        t2=TeamHave(name=n,number=0)
        db.session.add(t1)
        db.session.add(t2)
        db.session.commit()
    else:
        t1=TeamBelong.query.filter(TeamBelong.name==n).first()
    print(t1.id)
    print("\n\n\n\n")
    print(t1.name)
    t1.number=nrows
    for i in range(1, nrows):
        row_date = table.row_values(i)
        u1=User.query.filter(User.phone==row_date[0]).first()
        if u1 is None:
            new_user = User(name=row_date[1],password=row_date[2],phone=row_date[0])
            db.session.add(new_user)
            db.session.commit()
            ug=User_Goods()
            ug.user_id = new_user.id
            ug.TeamBelong_id = t1.id
            db.session.add(ug)
            db.session.commit()
        else:
            if User_Goods.query.filter(User_Goods.user_id==u1.id,User_Goods.TeamBelong_id==t1.id).first() is None:
                ug=User_Goods()
                ug.user_id = u1.id
                ug.TeamBelong_id = t1.id
                db.session.add(ug)
                db.session.commit()
    return jsonify({'status': 200, 'message': 'success','data':{'id':t1.id}})

