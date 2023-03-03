FROM python

COPY requirements.txt .
COPY facerec_using_face_distance.py .
ADD train_dir.tar /train_dir

RUN pip install cmake
RUN pip install dlib
RUN pip install -r requirements.txt

CMD ["python","facerec_using_face_distance.py"]