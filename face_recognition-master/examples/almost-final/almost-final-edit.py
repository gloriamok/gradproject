## 사진 encoding한 것을 담기 위한 배열 초기 설정

number_of_people = 10
number_of_photos = 20

encodings = [[0 for j in range(number_of_photos)] for i in range(number_of_people)]
names = [[0 for j in range(number_of_photos)] for i in range(number_of_people)]

order_ppl = 0

## 미리 200장의 사진을 encoding함

import face_recognition
import os

# Training directory
train_dir = os.listdir('train_dir/')

# Loop through each person in the training directory
for person in train_dir:
    pix = os.listdir("train_dir/" + person)
    order_pic = 0
    # Loop through each training image for the current person
    for person_img in pix:
        # Get the face encodings for the face in each image file
        face = face_recognition.load_image_file("train_dir/" + person + "/" + person_img)
        face_bounding_boxes = face_recognition.face_locations(face)
        #If training image contains exactly one face
        if len(face_bounding_boxes) == 1:
            face_enc = face_recognition.face_encodings(face)[0]
            # Add face encoding for current image with corresponding label (name) to the training data
            # encodings.append(face_enc)
            # names.append(person)
            encodings[order_ppl][order_pic] = face_enc
            names[order_ppl][order_pic] = person
        else:
            print(person + "/" + person_img + " was skipped and can't be used for training")
        order_pic += 1
    order_ppl += 1


## MySQL 연결 - DB server에 연결, 정상적으로 연결이 수립되면 커넥션 객체를 반환

from PIL import Image, ImageDraw
import numpy as np

import pymysql

#conn = pymysql.connect(host='localhost', user='root', password='1234', db='encore', charset='utf8')
conn = pymysql.connect(host='staff-db', user='staff', password='staff', db='testdb', charset='utf8')
#conn = pymysql.connect(host='localhost', user='sptest', password='sptest', db='testdb', charset='utf8')
# 커서 생성 - 커넥션 객체를 통해 데이터베이스에서 SQL문을 대신 실행해주고 결과를 반환해 줄 커서 객체를 생성한다.
cur = conn.cursor()

import base64
import io

############## 함수들

## 얼굴인식한 사진을 mysql에서 갖고 옴
def retriveImage(unknownId):
    sql = "SELECT unknownFace FROM Unknown WHERE unknownId=%s"
    cur.execute(sql, (unknownId,))
    results = cur.fetchall()
    # the returned data will be a list of list
    image = results[0][0]
    # Decode the string
    binary_data = base64.b64decode(image)
    #np.frombuffer(binary_data, dtype = np.float64)
    # Convert the bytes into a PIL image
    #image = Image.open(io.BytesIO(image))
    image = Image.open(io.BytesIO(binary_data))
    # Display the image using default image app
    # image.show()
    return image


## 얼굴인식 사진을 person_to_compare로 인코딩한 사진들과 비교
def face_recognition_result(image_to_test):
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)
    # print(len(image_to_test_encoding))
    if (len(image_to_test_encoding) == 0) :
        print("얼굴이 인식되지 않았습니다. 얼굴인식 프로그램을 종료합니다.")
        return

    '''
    import sys
    try:
        image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]
    except IndexError as e:
        print(e)
        print(unknownId + " FALSE")
        sys.exit(1)
    '''
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]

    # See how far apart the test image is from the known faces
    face_distances = face_recognition.face_distance(encodings_selected, image_to_test_encoding)

    total=0

    for i, face_distance in enumerate(face_distances):
        # print("The test image has a distance of {:.2} from known image #{}".format(face_distance, i))
        total += face_distance
        # print()

    print(total/20)
    print(1 - total/20)

    if (total/20 < 0.40):
        print(unknownId + " TRUE")
        print("\n" + unknownId + "가 맞습니다.")
    else:
        print(unknownId + " FALSE")
        print("\n" + unknownId + "가 아닙니다.")
    
    ## 얼굴 인식 완료한 사진 삭제
    sql = "DELETE FROM Unknown WHERE unknownId=%s"
    cur.execute(sql, (unknownId, ))
    conn.commit()
    print("\nDATA deleted succesfully")
    return
    
def face_check_execute():
    print("얼굴 인식 중...")
    ## 얼굴인식한 사람이 입력한 아이디를 가져옴
    sql = "SELECT * FROM Unknown"
    cur.execute(sql)
    row = cur.fetchone()
    if row != None:
        unknownId = row[0]
        print(unknownId)

        ## 이미 db에 저장되어있는 사진과
        ## 얼굴인식한 사람이 입력한 아이디의 사진과 비교
        ## 이미 db에 저장되어있는 사진들은 각각 encoding이 완료된 상태여야 함
        userId_dict = {"joohyuknam":"person_1", "yoojungkim":"person_2", "suzybae":"person_3", "bogumpark":"person_4", "jongsuklee":"person_5", "eunwoocha":"person_6", "yoonahim":"person_7", "jieunlee":"person_8", "jinyoungpark":"person_9", "minashin":"person_10"}
        person_to_compare = userId_dict[unknownId]
        print(person_to_compare)

        encodings_selected = []
        names_selected = []

        for idx, name in enumerate(names):
            if name[0] == person_to_compare:
                for face_enc, person in zip(encodings[idx], names[idx]):
                    encodings_selected.append(face_enc)
                    names_selected.append(person)

        print(names_selected)

        ## 얼굴인식한 사진을 mysql에서 갖고 옴
        unknown_Image = retriveImage(unknownId)
        #convert a PIL Image into a NumPy array
        unknown_Image2 = np.array(unknown_Image)

        ## 얼굴인식 사진을 person_to_compare로 인코딩한 사진들과 비교
        face_recognition_result(unknown_Image2)

        ## 얼굴 인식 완료한 사진 삭제
        # delete(unknownId)
    else:
        print("얼굴이 인식되지 않았습니다.")

########## 실행코드


# step1.관련 패키지 및 모듈 import
import schedule
import time

# step2.실행할 함수 선언
# def face_check_execute():

# step3.실행 주기 설정
schedule.every(10).seconds.do(face_check_execute)

# step4.스캐쥴 시작
while True:
    schedule.run_pending()
    time.sleep(1)

conn.close()