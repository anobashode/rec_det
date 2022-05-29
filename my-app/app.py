from copy import copy
import json
import numpy as np
import cv2
import sys 
import shutil
from wsgiref import headers
from flask import Flask, jsonify, request, render_template
from pyparsing import cpp_style_comment
app = Flask(__name__)
from flask_cors import CORS
from fc_det import detection
from fc_project import face_recog
from flask import request
import sys 
import requests
import os
import re

sys.path.append("C:\\users\\hiyak\\anaconda3\\lib\\site-packages")

import mysql.connector

CORS(app)

def detection(temppath):
    face_cascade = cv2.CascadeClassifier(r'C:\Users\hiyak\Downloads\haarcascade_frontalface_default.xml')

    address = sys.argv[0] 
    image = cv2.imread(temppath)
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(grey, 1.3, 5)

    if faces == ():
        return "false"
    else:
        return "true"


def downloadImage(self, file_path):
	print("downloading: " + self)
	img_data = requests.get(self).content
	print("File will be stored at:", file_path)
	with open(file_path, 'wb') as handler:
		handler.write(img_data)

def connect_db(query):
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="suga1993",
        database="prj_01_iit"
        #auth_plugin='mysql_native_password'
    )
    if db.is_connected():
        print("connected")
    cursor = db.cursor()

    print(query)
    query2='commit;'
    cursor.execute(query)
    cursor.execute(query2)


def select_db(query):
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="suga1993",
        database="prj_01_iit"
        #auth_plugin='mysql_native_password'
    )
    if db.is_connected():
        print("connected")
    cursor = db.cursor()

    print(query)
    cursor.execute(query)
    for row in cursor:
        return row


@app.route('/userdetails', methods = ["POST"])
def userdetails():
    print("home page")
    #data = request.data
    data_JSON = json.loads(str(request.data, encoding='utf-8'))
    #data_dict = json.loads(data_JSON)
    #dt=json.loads(str(data_JSON["data"], encoding='utf-8'))
    data_dict=data_JSON["data"]
    orderId=data_dict[0]["orderId"]
    name=data_dict[0]["name"]
    str_path=data_dict[0]["image"]
    #print(str_path)
    #print(name)
    #print(orderId)
    #print(insert_query)
    file_name=orderId+name+".jpg"
    temppath= os.path.join(os.path.dirname(__file__), 'validate', 'temp.jpg')
    fullpath = os.path.join(os.path.dirname(__file__), 'validate', file_name)
    downloadImage(str_path, temppath)
    flag=detection(temppath)
    if(flag=="true"):
        shutil.copy(temppath, fullpath)
        print(fullpath)
        fullpath_f= re.sub('\\\\',r'\\\\',fullpath)
        print('Copied')
        insert_query = "INSERT INTO PRJ_01_IIT.CONSIGNMENT_DETAIL (V_PACKAGE_ID, V_DEL_TO_NAME, V_DEL_TO_FACE) values( '"+orderId+"', '"+name+"', '"+fullpath_f+"') ON DUPLICATE KEY UPDATE V_DEL_TO_FACE = '"+fullpath_f+"';"
        connect_db(insert_query)
        return {'success': 'true', 'message': 'Uploaded Successfully'}
    else:
        return {'success': 'false', 'message': 'No face detected'}
   

@app.route('/validateOrderId', methods = ["GET"])
def validateOrderId():
    orderId = request.args.get('orderId')
    print(orderId)
    query_select="SELECT CASE WHEN DT.V_PACKAGE_ID IS NULL AND CD.V_PACKAGE_ID IS NOT NULL THEN 1 WHEN CD.V_PACKAGE_ID IS NULL THEN -1 ELSE 0 END AS FLAG, CASE WHEN CD.V_PACKAGE_ID IS NULL THEN 'Order ID doesn''t Exists' WHEN DT.V_PACKAGE_ID IS NULL AND CD.V_PACKAGE_ID IS NOT NULL THEN 'Order ID Exists and is not yet delivered' WHEN DT.V_PACKAGE_ID IS NOT NULL THEN 'Order ID Exists and is already delivered' END AS RESPONSE_STRING, GROUP_CONCAT(CD.V_DEL_TO_NAME) AS DELIVERY_TO_NAME_LIST FROM (SELECT SYSDATE() ) DL LEFT OUTER JOIN PRJ_01_IIT.CONSIGNMENT_DETAIL CD ON CD.V_PACKAGE_ID = '"+orderId+"' LEFT OUTER JOIN (SELECT DISTINCT V_PACKAGE_ID FROM PRJ_01_IIT.DELIVERED_TRANSACTIONS) DT ON CD.V_PACKAGE_ID = DT.V_PACKAGE_ID ORDER BY CD.V_DEL_TO_NAME;"
    row_ret = select_db(query_select)
    resp1=row_ret[0]
    resp2=row_ret[1]
    resp3=row_ret[2]
    print(resp1)
    print(resp2)
    print(resp3)
    if(str(resp1) == "0"):
        return {'success': 'false', 'message': resp2}
    elif(str(resp1) == "-1"):
        return {'success': 'false', 'message': resp2}
    else:
        return {'success': 'true', 'message': resp2, 'names': resp3}
    


app.run(debug=True)