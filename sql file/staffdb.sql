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
INSERT INTO User VALUES('joohyuknam', 'nam');
INSERT INTO User VALUES('yoojungkim', 'kim');
INSERT INTO User VALUES('suzybae', 'bae');
INSERT INTO User VALUES('bogumpark', 'park');
INSERT INTO User VALUES('jongsuklee', 'lee');
INSERT INTO User VALUES('eunwoocha', 'cha');
INSERT INTO User VALUES('yoonahim', 'im');
INSERT INTO User VALUES('jieunlee', 'lee');
INSERT INTO User VALUES('jinyoungpark', 'park');
INSERT INTO User VALUES('minashin', 'shin');