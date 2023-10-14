import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

cred = credentials.Certificate("face recog vsc/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://sih-hackathon-fbc24-default-rtdb.firebaseio.com/",
    'storageBucket': "sih-hackathon-fbc24.appspot.com"
})
bucket = storage.bucket()

cap = cv2.VideoCapture(0)
# cap.set(3,640)
# cap.set(4,480)
imgBackground = cv2.imread('Resources/background.png')

#IMPORTING THE MODE IMAGES INTO A LIST
folderModePath = 'Resources/Modes' 
modePath = os.listdir(folderModePath)
imgModeList = []
for path in modePath:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
   # print(len(imgModeList))

#Load the encoding file 
print("Loading Encode File...")
file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown,studentIds = encodeListKnownWithIds
print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success,img = cap.read()

    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS,faceCurFrame)
    
    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44+633,808:808+414] = imgModeList[modeType]
    
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1 , x2 , y2 , x1 = faceLoc
                y1 , x2 , y2 , x1 = y1*4 , x2*4 , y2*4 , x1*4
                bbox = 55+x1 , 162+y1 , x2 - x1 , y2- y1
                imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground,'Loading...',(275,400))
                    cv2.imshow("Face Attendence",imgBackground)
                    cv2.waitKey(1)
                    counter =1
                    modeType =1             

        if counter !=0:
            if counter == 1:
                #GET THE DATA 
                studentInfo = db.reference(f'Doctors/{id}').get()
                # print(studentInfo)
                #GET IMAGE FROM STORAGE
                # blob = bucket.get_blob(f'Images/{id}.png')
                # array = np.frombuffer(blob.download_as_string(),np.uint8)
                # imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                # update attendance
                # datetimeObject = datetime.strptime(studentInfo['last_attendence'],
                #                                 "%Y-%m-%d %H:%M:%S")
                # print("hi2")
                # secondElapsed=(datetime.now() - datetimeObject).total_seconds()
                # print(datetimeObject)
                # print(secondElapsed)
                # if secondElapsed>30:
                if matches[matchIndex]:
                    ref = db.reference(f'Doctors/{id}')
                    if studentInfo['in_hospital'] == False:
                        studentInfo['in_hospital'] = True
                        ref.child('in_hospital').set(studentInfo['in_hospital'])
                    else:
                        studentInfo['in_hospital'] = False
                        ref.child('in_hospital').set(studentInfo['in_hospital'])
                        studentInfo['total-attendance'] +=1


                    # if studentInfo['in_hospital'] == True:
                        # studentInfo['in_hospital'] = False
                        # ref.child('in_hospital').set(studentInfo['in_hospital'])
                    
                    
                        # studentInfo['total-attendance'] +=1
                    ref.child('total-attendance').set(studentInfo['total-attendance'])
                    ref.child('last_attendence').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S "))
                else:
                    modeType=3
                    counter=0
                    imgBackground[44:44+633 , 808:808+414] = imgModeList[modeType]

        if modeType !=3:
            if 10<counter<20:
                modeType = 2
            imgBackground[44:44+633 , 808:808+414] = imgModeList[modeType]
        
            if counter<= 10:
                cv2.putText(imgBackground,str(studentInfo['total-attendance']),(861,125),
                            cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                cv2.putText(imgBackground,str(studentInfo['major']),(1006,550),
                            cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                cv2.putText(imgBackground,str(id),(1006,493),
                            cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                cv2.putText(imgBackground,str(studentInfo['standing']),(910,625),
                            cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                cv2.putText(imgBackground,str(studentInfo['year']),(1025,625),
                            cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                # cv2.putText(imgBackground,str(studentInfo['starting_year']),(1125,625),
                #             cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                cv2.putText(imgBackground,str(studentInfo['in_hospital']),(1125,625),
                            cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                
                
                (w,h), _ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                offset = (414 -w)//2
                cv2.putText(imgBackground,str(studentInfo['name']),(808+offset,445), cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
                
            # imgBackground[175:175+216,909:909+216] = imgStudent  
            
        
            counter += 1

            if counter >= 30:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0

        
   
    #cv2.imshow("WebCam",img)
    cv2.imshow("Face Attendence",imgBackground)
    cv2.waitKey(1)
     
