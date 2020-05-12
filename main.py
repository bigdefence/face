# -*- coding: utf-8 -*-
import flask
from flask import Flask, request, render_template
import numpy as np
import sys
import cv2
import requests
import imutils
import os
import pickle
import imageio
import json
app = Flask(__name__)


# 메인 페이지 라우팅
@app.route("/")
@app.route("/index")
def index():
    return flask.render_template('index.html')


# 데이터 예측 처리
@app.route('/predict', methods=['POST'])
def make_prediction():
    if request.method == 'POST':

        # 업로드 파일 처리 분기
        file = request.files['image'].read()
        if not file: return render_template('index.html', label="No Files")
        client_id = "cqEqZRrO2Eu_SZX_9Nv0"
        client_secret = "9pe7QYe1JH"
        #url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지
        url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식
        files = {'image': file}
        headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
        response = requests.post(url,  files=files, headers=headers)
        rescode = response.status_code
        if(rescode==200):
            data=json.loads(response.text)
            if data['faces'][0]['celebrity']['value']:
                label=data['faces'][0]['celebrity']['value']
            else:
                label='등록된 사진을 인식할 수 없습니다.'        
        else:
            print("Error Code:" + rescode)
        return render_template('index.html', label=label)


if __name__ == '__main__':

    # Flask 서비스 스타트
    app.run(host='0.0.0.0')
