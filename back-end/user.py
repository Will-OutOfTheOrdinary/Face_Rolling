from flask import Flask,request,jsonify
import re
import numpy as np
import math
import random
from flask_sqlalchemy import SQLAlchemy
from model import app,db,User
from flask import Blueprint
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest
import redis
user_api = Blueprint('user_app', __name__)
credentials = AccessKeyCredential('LTAI5tMpq1bfR6YwU97G1XY5', 'UY6Dfu2KxN1gmp7nz3V5jLwvLA6lZQ')
client = AcsClient(region_id='cn-hangzhou', credential=credentials)



pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
rd=redis.Redis(connection_pool=pool)
def phonecheck(s):
    phoneprefix=['130','131','132','133','134','135','136','137','138','139','150','151','152','153','156','158','159','170','180','183','182','185','186','188','189']
    if len(s)>11 or len(s)<11: 
        return False
    else:
        if  s.isdigit():
            if s[:3] in phoneprefix:
                return True
            else:
                return False
        else:
            return False


@app.route('/login',methods=['POST'])
def login():
    name = request.form.get("name")
    password = request.form.get("password")
    a={
        "id":-1,
        "name":"",
        "password":"",
        "account":"",
        'phone':"",
        "avatarUrl":"",
        "joinInTeam":""
    }
    if not all([name,password]):
        return jsonify({'status': 400, 'message': '参数不完整', 'data': a})
    u = User.query.filter(User.name==name,User.password==password).first()
    if u is None:
        return jsonify({'status': 404, 'message': '用户名或者密码错误','data':a})
    recs=u.images
    ans={
            "id":u.id,
            "name":u.name,
            "password":u.password,
            "account":u.phone,
            'phone':u.phone,
            "avatarUrl":'images/avatar_default.png',
            "joinInTeam":""
        }
    for rec in recs:
        ans={
            "id":u.id,
            "name":u.name,
            "password":u.password,
            "account":u.phone,
            'phone':u.phone,
            "avatarUrl":rec.path,
            "joinInTeam":""
        }
        #break
    bs=u.teambelongs
    xx=[]
    for b in bs:
        vi={'id':b.id,'name':b.name}
        xx.append(vi)
    ans['joinInTeam']=xx
    return jsonify({'status': 200, 'message': 'success', 'data': ans})
    
@app.route('/register',methods=['POST'])
def register():
    phone=request.form.get('phone')
    verification=request.form.get('verification')
    username = request.form.get('name')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    u={
            'id':-1,
            'name' : "",
            'password' : ""
    }
    if not all([username,password1,password2,phone,verification]):
        return jsonify({'status': 400, 'message': '参数不完整', 'data': u})
    elif password1 != password2:
        return jsonify({'status': 400, 'message': '两次密码不一致，请重新输入', 'data': u})
    elif User.query.filter_by(name=username).all():
        return jsonify({'status': 400, 'message': '用户名已存在', 'data': u})
    elif User.query.filter_by(phone=phone).all():
        return jsonify({'status': 400, 'message': '手机号已存在', 'data': u})
    elif verification!=rd.get(phone):
       return jsonify({'status': 400, 'message': '验证码错误', 'data': u})
    else:
        new_user = User(name=username,password=password1,phone=phone)
        db.session.add(new_user)
        db.session.commit()
        use={
            'id':new_user.id,
            'name' : username,
            'password' : password1
        }
        return jsonify({'status': 201, 'message': 'success', 'data': use})
    
def get_code():
    code = ''
    for i in range(6):
        add = random.randint(0, 9)
        code += str(add)
    return code

@app.route('/getVerification',methods=['POST'])
def getVerification():
    tel=request.form.get('phone')
    u={
        'telephone':"",
        'code':""
    }
    if tel is None:
        return jsonify({'status': 400, 'message': '手机号为空', 'data': u})
    if phonecheck(tel) is False:
        return jsonify({'status': 400, 'message': '手机号错误', 'data': u})
    code=get_code()
    request1 = SendSmsRequest()
    request1.set_accept_format('json')
    request1.set_SignName("阿里云短信测试")
    request1.set_TemplateCode("SMS_154950909")
    request1.set_PhoneNumbers(tel)
    request1.set_TemplateParam("{\"code\":\""+code+"\"}")

    response = client.do_action_with_exception(request1)
    if 'OK' in str(response):
        rd.set(tel,code,ex=300)
        use={
            'telephone':tel,
            'code':code
        }
        return jsonify({'status': 200, 'message': '成功发送', 'data': use})
    else:
        return jsonify({'status': 400, 'message': '发送失败', 'data': u})
    
    
@app.route('/getPersonalInfor',methods=['POST'])
def getPersonalInfor():
    idd=request.form.get('id')
    u=User.query.get(idd)
    a={
        "id":-1,
        "name":"",
        "password":"",
        "account":"",
        'phone':"",
        "avatarUrl":"",
        "joinInTeam":""
    }
    if u is None:
        return jsonify({'status': 404, 'message': '无此用户','data':a})
    recs=u.images
    ans={
            "id":u.id,
            "name":u.name,
            "password":u.password,
            "account":u.phone,
            'phone':u.phone,
            "avatarUrl":'images/avatar_default.png',
            "joinInTeam":""
        }
    for rec in recs:
        ans={
            "id":u.id,
            "name":u.name,
            "password":u.password,
            "account":u.phone,
            'phone':u.phone,
            "avatarUrl":rec.path,
            "joinInTeam":""
        }
        #break
    bs=u.teambelongs
    xx=[]
    for b in bs:
        vi={'id':b.id,'name':b.name}
        xx.append(vi)
    ans['joinInTeam']=xx
    return jsonify({'status': 200, 'message': 'success', 'data': ans})
