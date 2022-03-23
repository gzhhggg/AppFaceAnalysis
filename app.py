from importlib.resources import path
from pathlib import Path
from unittest import result
from flask import Flask, request, redirect, render_template, flash
import pandas as pd
import numpy as np
import cv2
import os
import json
from werkzeug.utils import secure_filename

import requests

#アップロードされた画像を保存するフォルダ名とアップロードを許可する拡張子
SAVE_FOLDER = "./static/save_images"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# APIkeyの取得
def get_api_key():
    api_path = os.path.join("./static/json","secret.json")
    with open(api_path) as f:
        secret_json = json.load(f)
        FaceApiKey = secret_json['SUBSCRIPTION_KEY']
        Endpoint = secret_json['ENDPOINT']
    return FaceApiKey , Endpoint

#face_APIから情報の取得
def search_face(filepath):
    FaceApiKey , Endpoint = get_api_key()
    assert FaceApiKey
    face_api_url = Endpoint + '/face/v1.0/detect'

    headers = {
        'Content-Type':'application/octet-stream',
        'Ocp-Apim-Subscription-Key': FaceApiKey}

    params = {
        'recognitionModel': "recognition_04",
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,makeup,emotion,hair,occlusion,accessories,blur,exposure,noise'
    }

    with open(filepath,'rb') as f:
        binary_img = f.read()

    res = requests.post(face_api_url, params=params,
                        headers=headers, data= binary_img)
    results= res.json()
    return results

#画像の前処理
def preprocessing_img(results,filepath):
    df_pre = pd.DataFrame()
    df_pre = pd.json_normalize(results)
    img = cv2.imread(filepath)
    img_rect = img.copy()
    filename = os.path.basename(filepath)
    filename_noex = os.path.splitext(filename)[0]
    df_pre = df_pre.astype('int',errors = 'ignore')
    img_list = []
    base_save_path = os.path.join(SAVE_FOLDER , filename_noex + "_base.jpg")
    for index,d in df_pre.iterrows():
        angle = d["faceAttributes.headPose.roll"]
        x = d["faceRectangle.left"]
        y = d["faceRectangle.top"]
        w = d["faceRectangle.width"]
        h = d["faceRectangle.height"]
        center_x , center_y = (x + w/2),(y + h/2)
        x_start = center_x - w
        x_end = x_start + w * 2
        y_start = center_y - h
        y_end = y_start + h * 2
        face_cut = img[int(y_start):int(y_end), int(x_start):int(x_end)]
        # 角度の修正
        height,width = face_cut.shape[:2]
        center = (int(width/2), int(height/2))
        radians = np.deg2rad(angle)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        new_width = int(abs(np.sin(radians)*height) + abs(np.cos(radians)*width))
        new_height = int(abs(np.sin(radians)*width) + abs(np.cos(radians)*height))
        M[0,2] += int((new_width-width)/2)
        M[1,2] += int((new_height-height)/2)
        rol_img = cv2.warpAffine(face_cut, M, (new_width, new_height))
        reslult_img = cv2.resize(rol_img , (150, 150))
        content_save_path = os.path.join(SAVE_FOLDER , filename_noex + "_" + str(index) + ".jpg")
        img_list.append(content_save_path)
        # 元画像に四角枠追加
        img_rect = cv2.rectangle(img_rect,(x,y),((x+w),(y+h)),(0, 0, 255), thickness=2)
        cv2.imwrite(content_save_path,reslult_img)
    cv2.imwrite(base_save_path,img_rect)
    return img_list ,base_save_path

#グラフの前処理
def preprocessing_graph(results):
    df_pre = pd.DataFrame()
    df_pre = pd.json_normalize(results)
    df = pd.DataFrame()    
    #詳細情報
    df['sex'] = df_pre["faceAttributes.gender"].apply(lambda x: "男性" if x == "male" else "女性")
    df['age'] = df_pre['faceAttributes.age'].astype(int)
    df['smile'] = (df_pre['faceAttributes.smile']*100).astype(int)
    df['glasses'] = df_pre['faceAttributes.glasses'].apply(lambda x:"無" if x == "NoGlasses" else "有")
    df['noise'] = df_pre['faceAttributes.noise.noiseLevel'].apply(lambda x:"高い" if x == "low" else("普通" if x == "medium" else "低い"))
    df['moustache'] = (df_pre['faceAttributes.facialHair.moustache']*100).astype(int)
    df['eyemakeup'] = df_pre['faceAttributes.makeup.eyeMakeup'].apply(lambda x: "無" if x == False else "有")
    df['lipmakeup'] = df_pre['faceAttributes.makeup.lipMakeup'].apply(lambda x: "無" if x == False else "有")
    df['mask'] = df_pre['faceAttributes.occlusion.mouthOccluded'].apply(lambda x: "無" if x == False else "有")
    df['cap'] = df_pre['faceAttributes.hair.invisible'].apply(lambda x: "無" if x == False else "有")

    # 表情分析
    df['emotion_anger'] = (df_pre['faceAttributes.emotion.anger']*100).astype(float)
    df['emotion_contempt'] = (df_pre['faceAttributes.emotion.contempt']*100).astype(float)
    df['emotion_disgust'] = (df_pre['faceAttributes.emotion.disgust']*100).astype(float)
    df['emotion_fear'] = (df_pre['faceAttributes.emotion.fear']*100).astype(float)
    df['emotion_happiness'] = (df_pre['faceAttributes.emotion.happiness']*100).astype(float)
    df['emotion_neutral'] = (df_pre['faceAttributes.emotion.neutral']*100).astype(float)
    df['emotion_sadness'] = (df_pre['faceAttributes.emotion.sadness']*100).astype(float)
    df['emotion_surprise'] = (df_pre['faceAttributes.emotion.surprise']*100).astype(float)

    # 髪色分析
    df_hair = pd.json_normalize(df_pre['faceAttributes.hair.hairColor'])
    for index, rows in df_hair.iterrows():
        for row in rows:
            try:
                buf = row['color']
                df.at[index,buf] = float(row['confidence'])*100
            except:
                continue
    return df

#Flaskクラスのインスタンスの作成
app = Flask(__name__)

#アップロードされたファイルの拡張子のチェックをする関数
def allowed_file(filepath):
    return '.' in filepath and filepath.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            answer = "ファイルがありません"
            return  render_template("index.html",answer = answer)
        file = request.files['file']
        if file.filename == '':
            answer = "ファイルがありません"
            return  render_template("index.html",answer = answer)

        if file and allowed_file(file.filename):
            filepath = secure_filename(file.filename)
            file.save(os.path.join(SAVE_FOLDER, filepath))
            filepath = os.path.join(SAVE_FOLDER, filepath)
            # ここから前処理
            results = search_face(filepath)
            if results ==[]:
                answer = "顔が検出されませんでした"
                return render_template("index.html",answer = answer)

            list_img , base_savepath = preprocessing_img(results , filepath)
            df_graph = preprocessing_graph(results)
            df_graph["file_path"] = list_img
            df = pd.DataFrame()
            df = df_graph.values.tolist()
            return render_template("results.html",df = df , base_savepath = base_savepath)
        else:
            answer = "拡張子が対応されていません"
            return render_template("index.html",answer = answer)
    return render_template("index.html",answer = "")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)