## 사진 encoding한 것을 담기 위한 배열 초기 설정

number_of_people = 10
number_of_photos = 20

encodings = [[0 for j in range(number_of_photos)] for i in range(number_of_people)]
names = [[0 for j in range(number_of_photos)] for i in range(number_of_people)]

order_ppl = 0

## 미리 200장의 사진을 encoding함

import face_recognition
import os

# import time
# start = time.time()

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

# print("time :", time.time() - start)
# print(names)


## MySQL 연결 - DB server에 연결, 정상적으로 연결이 수립되면 커넥션 객체를 반환

from PIL import Image, ImageDraw
import numpy as np

import pymysql

#conn = pymysql.connect(host='localhost', user='root', password='1234', db='encore', charset='utf8')
conn = pymysql.connect(host='localhost', user='sptest', password='sptest', db='testdb', charset='utf8')
# 커서 생성 - 커넥션 객체를 통해 데이터베이스에서 SQL문을 대신 실행해주고 결과를 반환해 줄 커서 객체를 생성한다.
cur = conn.cursor()
# 데이터 조회 - 커서에 SELECT로 조회한 결과를 한꺼번에 저장
# sql = 'select * from departments where department_id=%s'
# vals = (department_id,)
# cur.execute(sql, vals)
# sql = "SELECT * FROM USER"
# cur.execute(sql)

# 조회결과를 커서에서 fetch - 조회한 데이터를 커서객체에서 한 행씩 접근하여 출력
# 여러 줄 출력
# for row in cur:
#     print(row[0], row[1])


## 웹페이지에서 하는 일
## 얼굴인식한 사진을 mysql DB의 Unknown table에 저장

# MySQL에 이미지 저장
import base64
import io

def convert(filename):
    with open(filename, 'rb', encoding='UTF-8') as file:
        binary = file.read()
        binary = base64.b64encode(binary)
    return binary

def insert_unknown(unknownId,photo):
    photo = convert(photo)
    sql = "INSERT INTO UNKNOWN (unknownId, unknownFace) VALUES(%s,%s)"
    cur.execute(sql, (unknownId, photo))
    conn.commit()
    print("\nDATA inserted succesfully")
    return 0

# insert_unknown("joohyuknam","test\\gray.jpg")

## 얼굴인식한 사람이 입력한 아이디를 가져옴
sql = "SELECT * FROM UNKNOWN"
cur.execute(sql)
row = cur.fetchone()
unknownId = row[0]
print(unknownId)

## 이미 db에 저장되어있는 사진과
## 얼굴인식한 사람이 입력한 아이디의 사진과 비교
## 이미 db에 저장되어있는 사진들은 각각 encoding이 완료된 상태여야 함***
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

# print(names_selected)



## 얼굴인식한 사진을 mysql에서 갖고 옴

# import sys

def retriveImage(unknownId):
    sql = "SELECT unknownFace FROM UNKNOWN WHERE unknownId=%s"
    cur.execute(sql, (unknownId,))
    results = cur.fetchall()
    # the returned data will be a list of list
    image = results[0][0]
    # Decode the string
    binary_data = base64.b64decode(image)
    #np.frombuffer(binary_data, dtype = np.float64)
    # Convert the bytes into a PIL image
    #image = Image.open(io.BytesIO(image), encoding='UTF-8')
    image = Image.open(io.BytesIO(binary_data), encoding='UTF-8')
    # Display the image using default image app
    image.show()
    return image

unknown_Image = retriveImage(unknownId)

#convert a PIL Image into a NumPy array
unknown_Image2 = np.array(unknown_Image)


# 얼굴인식 사진을 person_to_compare로 인코딩한 사진들과 비교
def face_recognition_result(image_to_test):
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)
    # print(len(image_to_test_encoding))
    if (len(image_to_test_encoding) == 0) :
        print("얼굴이 인식되지 않았습니다. 얼굴인식 프로그램을 종료합니다.")
        return
    
    '''
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
    else:
        print(unknownId + " FALSE")

## 얼굴 인식 완료한 사진 삭제

face_recognition_result(unknown_Image2)

def delete(unknownId):
    sql = "DELETE FROM UNKNOWN WHERE UNKNOWNID=%s"
    cur.execute(sql, (unknownId, ))
    conn.commit()
    print("\nDATA deleted succesfully")
    return 0

delete(unknownId)