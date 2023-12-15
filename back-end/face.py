from flask import Flask,request,jsonify
import re
import numpy as np
import math
import cv2
from flask_sqlalchemy import SQLAlchemy
from model import app,db,User,ImageFile,TeamBelong
from flask import Blueprint
from sqlalchemy import desc 
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

face_api = Blueprint('face_app', __name__,static_folder='images')

@app.route('/connectImageToPerson', methods=['POST'])
def connectImageToPerson():
    img=request.files.get("image")
    person_id=request.form.get("person_id")
    file_path=None
    if img is not None:
        nnn=img.filename.split('.')
        nx=ImageFile.query.order_by(desc(ImageFile.id)).first()
        if nx is not None:
            idd=nx.id+1
        else:
            idd=1
        file_path = "images/"+str(idd)+"."+nnn[-1]
        new_img=ImageFile(path=file_path,image_name=str(idd)+"."+nnn[-1],user_id=person_id)
        db.session.add(new_img)
        img.save("./"+file_path)
        db.session.commit()
        u = User.query.get(person_id)
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
        return jsonify({'status': 200, 'message': 'success','data':ans})
    else:
        return jsonify({'status': 404, 'message': '没图片'})

@app.route('/FaceReconize', methods=['POST'])
def FaceReconize():
    img1=request.files.get("together_image")
    td=request.form.get("team_id",type=int)
    x=[]
    x.append('黄元奎')
    x.append('孙振翔')
   # return jsonify({'status':200,'message':'success','data':{'late':x,'percent':"60%",'id':td}})
    img1.save("./group.jpg")
    app = FaceAnalysis(providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=-1, det_size=(640, 640))
    img = cv2.imread('./group.jpg')
    
    faces = app.get(img)
    feats = []
    for face in faces:
        feats.append(face.normed_embedding)
    if len(feats)==0:
        return jsonify({'status':404,'message':'no body','data':{'late':[],'percent':"",'id':td}})
    feats = np.array(feats, dtype=np.float32)
    team=TeamBelong.query.get(td)
    uss=team.users
    late=[]
    for u in uss:
        ax=u.images
        if ax is None:
            late.append(u.id)
            continue
        for a in ax:
            file_path=a.path
            target = cv2.imread("./"+file_path)
            target_faces = app.get(target)
            if len(target_faces)==0:
                continue
            target_feat = np.array(target_faces[0].normed_embedding, dtype=np.float32)
            sims = np.dot(feats, target_feat)
            target_index = int(sims.argmax())
            check=False
            if(sims[target_index]>=0.5):
                check=True
            if check== False:
                late.append(u.name)
            break
    percent=(len(uss)-len(late))*1.0/len(uss)*100
    percent=str(percent)+"%"
    return jsonify({'status': 200, 'message': 'success', 'data':{'late':late,'percent':percent,'id':td}})
