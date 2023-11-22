## 쿠버네티스 클러스터 환경에서의 얼굴인식 기반 출입관리 시스템 개발
> Development of Face Recognition based Access Control System in Kubernetes Cluster Environment


## 기획 배경 (기대 효과)
- 기존의 출입관리 시스템은:
  * 서버에 있는 데이터의 수정이 까다롭고 무중단 업데이트가 불가능해 오랜 시간과 높은 인건비가 발생합니다.
  * 서버에 문제가 생길 경우, 연결되어있는 시스템까지 장애가 생겨 관리자가 직접 그 장애를 복구해야 합니다.
  * 출입을 위한 인증이 아이디, 비밀번호나 카드, QR코드 등으로 되어있어서 아이디와 비밀번호가 노출되면 인가되지 않은 사용자가 출입할 가능성이 있다는 보안적인 이슈가 있습니다.
- **쿠버네티스 클러스터 환경**에서의 **얼굴인식 기반** 출입관리 시스템은:
  * **무중단 업데이트**가 가능합니다.
  * **시스템 자동 복구**가 가능합니다.
  * **빠르고 간편한 출입**이 가능하고 **2단계 인증**을 통해 시스템의 보안을 강화합니다.


## 시스템 전체 구조
쿠버네티스 클러스터 환경에서의 얼굴인식 기반 출입관리 시스템의 전체 구조는 다음과 같습니다.
![image](images/system-structure.png)


## 웹 페이지
웹 페이지에서 아이디/비밀번호 로그인과 얼굴인식을 수행할 수 있습니다.
![image](images/weblogin-and-face-rec.jpg)


## 데이터베이스
아이디/비밀번호가 저장되어있고, 웹에서 찍은 사진이 저장됩니다.
![image](images/web-and-db.png)


## 얼굴인식
관계자 이미지와 웹에서 찍은 사진을 비교하여 얼굴인식 결과를 도출합니다.
![image](images/face-recognition.png)


## 아두이노로 결과 출력
얼굴인식 결과를 전송받아 출력합니다.
![image](images/arduino.png)
얼굴인식 모듈과 결과 출력 모듈의 상호작용
![image](images/door-open-and-close.png)
쿠버네티스 환경에서 결과 출력 모듈 실행 결과 ((왼쪽부터) 수신한 문자 없음/ T/ F)


## 도커 이미지 버전
* 도커 어플리케이션 이미지를 도커와 쿠버네티스 환경에 맞게 빌드하여 관리합니다.
* 이미지는 DockerHub의 [gloriamok/python-face-rec](https://hub.docker.com/r/gloriamok/python-face-rec/tags)에서 다운받을 수 있습니다.
![image](images/docker-image-version.png)
