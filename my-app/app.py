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
from fc_project import face_recog
from flask import request
import sys 
import requests
import os
import re
from fc_project import face_recog
import face_recognition
import cv2
import numpy as np
import sys

sys.path.append("C:\\users\\hiyak\\anaconda3\\lib\\site-packages")

import mysql.connector

CORS(app)

def face_recog(str_path):
    video_capture = cv2.VideoCapture(0)

    # eyes_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

    address = sys.argv[0]
    #query = "select * from prj_01_iit.test_1;"
    #cursor.execute(query)
    #for row in cursor:
    #    print("data {}".format(row))
    #path_img = row
    hiya_image = face_recognition.load_image_file(str_path)
    hiya_face_encoding = face_recognition.face_encodings(hiya_image)[0]

    # yukta_image = face_recognition.load_image_file(r"C:\Users\hiyak\Downloads\yukta.jpeg")
    # yukta_face_encoding = face_recognition.face_encodings(yukta_image)[0]

    # yashvardhan_image = face_recognition.load_image_file("yash.jpeg")
    # yashvardhan_face_encoding = face_recognition.face_encodings(yashvardhan_image)[0]


    known_face_encodings = [
        hiya_face_encoding
        # , yashvardhan_face_encoding
        
    ]
    known_face_names = [
        "Hiya"
        # , "Yash"
    ]


    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    flag = False 
    count_names ={}
    flag2=False

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # obtaining the gray picture
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            # When face is detected
            if face_locations!= []:
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    else:
                        name = "Unknown"

                    face_names.append(name)
                    if name in count_names:
                        count_names[name]+=1
                    else:
                        count_names[name] = 1

                
                    print(face_names)
                    
                    if "Unknown" in count_names.keys():
                        if count_names["Unknown"] >5:
                            print("Sorry, couldn't recognise you!")
                            flag2 = True

                    if "Hiya" in count_names.keys():
                        if count_names["Hiya"] >3:
                            print("success")
                            flag = True
                    
                    
                    
            #Masked face/ When face is not detected
            # else:
            #     flag = False
            # else:
            #     eyes_in_faces = eyes_cascade.detectMultiScale(gray, 1.3, 5 )
            #     try:
            #         for (ex, ey, ew, eh) in eyes_in_faces:
            #             top_left=(ex-ew, ey-eh)
            #             bottom_right=((ex+2*ew), (ey+2*eh))
            #         cv2.rectangle(frame, top_left , bottom_right, (0, 0, 255), 2)
            #     except:
            #         pass

                    # cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        
                

        # Display the resulting image
        cv2.imshow('Video', frame)
        


        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if flag2==True:
            break
        
        if flag==True:
            #q_update_delivery_nm="update schema_name.table_name colname='HIYA' where col_name_pk='package_id'"
            #cursor = connect_db(q_update_delivery_nm)
            break
        
        # elif flag==False==flag2:
        #     print("No face Found!")
        #     break


    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

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
    
@app.route('/validateDelivery', methods = ["GET"])
def validateDelivery():
    orderId = request.args.get('orderId')
    print(orderId)
    str_path=r"C:\done\my-app\src\validate\hiya.jpeg"
    fl=face_recog(str_path)
    if(fl == "false"):
        return {'success': 'false', 'message': "Invalid user."}
    elif(fl == "true"):
        return {'success': 'true', 'message': "Valid User."}

app.run(debug=True)