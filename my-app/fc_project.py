import face_recognition
import cv2
import numpy as np
import sys
from flask import flash

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)

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
                            flash("Sorry, couldn't recognise you!")
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
    return flag2