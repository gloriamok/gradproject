-- 테이블 생성
use testdb;
Drop TABLE User;
Drop TABLE Unknown;

CREATE TABLE User (
  userId      VARCHAR(40),
  userPw    VARCHAR(40)
);

CREATE TABLE Unknown (
  unknownId      VARCHAR(40),
  unknownFace  MEDIUMBLOB
);

-- 데이터 생성
INSERT INTO User VALUES('jooyoungmok', 'mok');
INSERT INTO User VALUES('sangmilee', 'lee');
INSERT INTO User VALUES('chaeyuncho', 'cho');
INSERT INTO User VALUES('heesoolee', 'lee');


# select * from user;
select * from unknown;
# truncate table unknown;