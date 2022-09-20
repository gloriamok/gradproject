## ���� encoding�� ���� ��� ���� �迭 �ʱ� ����

number_of_people = 10
number_of_photos = 20

encodings = [[0 for j in range(number_of_photos)] for i in range(number_of_people)]
names = [[0 for j in range(number_of_photos)] for i in range(number_of_people)]

order_ppl = 0

## �̸� 200���� ������ encoding��

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


## MySQL ���� - DB server�� ����, ���������� ������ �����Ǹ� Ŀ�ؼ� ��ü�� ��ȯ

from PIL import Image, ImageDraw
import numpy as np

import pymysql

#conn = pymysql.connect(host='localhost', user='root', password='1234', db='encore', charset='utf8')
conn = pymysql.connect(host='localhost', user='sptest', password='sptest', db='testdb', charset='utf8')
# Ŀ�� ���� - Ŀ�ؼ� ��ü�� ���� �����ͺ��̽����� SQL���� ��� �������ְ� ����� ��ȯ�� �� Ŀ�� ��ü�� �����Ѵ�.
cur = conn.cursor()
# ������ ��ȸ - Ŀ���� SELECT�� ��ȸ�� ����� �Ѳ����� ����
# sql = 'select * from departments where department_id=%s'
# vals = (department_id,)
# cur.execute(sql, vals)
# sql = "SELECT * FROM USER"
# cur.execute(sql)

# ��ȸ����� Ŀ������ fetch - ��ȸ�� �����͸� Ŀ����ü���� �� �྿ �����Ͽ� ���
# ���� �� ���
# for row in cur:
#     print(row[0], row[1])


## ������������ �ϴ� ��
## ���ν��� ������ mysql DB�� Unknown table�� ����

# MySQL�� �̹��� ����
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

## ���ν��� ����� �Է��� ���̵� ������
sql = "SELECT * FROM UNKNOWN"
cur.execute(sql)
row = cur.fetchone()
unknownId = row[0]
print(unknownId)

## �̹� db�� ����Ǿ��ִ� ������
## ���ν��� ����� �Է��� ���̵��� ������ ��
## �̹� db�� ����Ǿ��ִ� �������� ���� encoding�� �Ϸ�� ���¿��� ��***
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



## ���ν��� ������ mysql���� ���� ��

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


# ���ν� ������ person_to_compare�� ���ڵ��� ������� ��
def face_recognition_result(image_to_test):
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)
    # print(len(image_to_test_encoding))
    if (len(image_to_test_encoding) == 0) :
        print("���� �νĵ��� �ʾҽ��ϴ�. ���ν� ���α׷��� �����մϴ�.")
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

## �� �ν� �Ϸ��� ���� ����

face_recognition_result(unknown_Image2)

def delete(unknownId):
    sql = "DELETE FROM UNKNOWN WHERE UNKNOWNID=%s"
    cur.execute(sql, (unknownId, ))
    conn.commit()
    print("\nDATA deleted succesfully")
    return 0

delete(unknownId)