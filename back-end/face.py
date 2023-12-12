from flask import Flask,request,jsonify
import re
import numpy as np
import math
import cv2
from flask_sqlalchemy import SQLAlchemy
from model import app,db,User,ImageFile
from flask import Blueprint
from sqlalchemy import desc 
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

face_api = Blueprint('face_app', __name__,static_folder='images')

@app.route('/takePhoto/', methods=['POST'])
def takePhoto():
    img=request.files.get("photo")
    file_path=None
    if img is not None:
        nnn=img.filename.split('.')
        nx=ImageFile.query.order_by(desc(ImageFile.id)).first()
        if nx is not None:
            idd=nx.id+1
        else:
            idd=1
        file_path = "images/"+str(idd)+"."+nnn[-1]
        new_img=ImageFile(image=img,path=file_path,image_name=str(idd)+"."+nnn[-1])
        db.session.add(new_img)
        img.save("./"+file_path)
        if nnn[-1]=='jpg' or nnn[-1]=='png':
            immg=cv2.imread("./"+file_path)
            a=math.ceil(math.sqrt((immg.shape[0]*immg.shape[1])/1000000))
            y=int(immg.shape[0]/a)
            x=int(immg.shape[1]/a)
            immg=cv2.resize(immg,(x,y))
            cv2.imwrite("./"+file_path,immg)
        db.session.commit()
    return jsonify({'status': 200, 'message': 'success'})

@app.route('/face_recognize/', methods=['POST'])
def face_recognize():
    img1=request.files.get("image1")
    img2=request.files.get("image2")
    img1.save("./img1.jpg")
    img2.save("./img2.jpg")
    app = FaceAnalysis(providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=-1, det_size=(640, 640))
    img = cv2.imread('img1.jpg')
    faces = app.get(img)
    feats = []
    for face in faces:
        feats.append(face.normed_embedding)
    feats = np.array(feats, dtype=np.float32)
    target = cv2.imread("img2.jpg")
    target_faces = app.get(target)   
    target_feat = np.array(target_faces[0].normed_embedding, dtype=np.float32)
    sims = np.dot(feats, target_feat)
    target_index = int(sims.argmax())
    check=False
    if(sims[target_index]>=0.5):
        check=True
    return jsonify({'status': 200, 'message': 'success', 'check':check})