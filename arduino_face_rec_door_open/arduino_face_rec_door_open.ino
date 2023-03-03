#include<LiquidCrystal.h>
#include<Wire.h>
#include<Servo.h> //Servo 라이브러리를 추가

LiquidCrystal lcd(3, 4, 9, 10, 11, 12);  //(RS, E, DB4, DB5,DB6,DB7)
Servo servo;      //Servo 클래스로 servo객체 생성
char cmd;

int greenLED = 5;
int redLED = 6;
int servo_Pin = 7;
int min_value = 544;  //펄스폭 최소값 0도
int max_value = 2400; //펄스폭 최대값 180도

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  digitalWrite(greenLED, LOW);
  digitalWrite(redLED, LOW);
  lcd.begin(16,2);    //디스플레이가 가진 행과 열 정보
  lcd.clear();
  lcd.setCursor(0,0);   //lcd 시작 (0,0)
  lcd.print("This is ");
  lcd.setCursor(0,1);
  lcd.print("DOOR OPEN system");
  servo.attach(servo_Pin,min_value,max_value);     //servo 서보모터 7번 핀에 연결
  servo.write(180); //servo모터 중심 찾기

}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){//pc로부터 시리얼통신 전송되면, 한줄씩 읽어와서 cmd변수에 입력
    cmd = Serial.read();
    //lcd.setCursor(0,0);
    //lcd.write("Sensing...");
    if(cmd == 't'){ //파이썬으로부터 true 전달되면 green led ON
      Serial.println("아두이노: 켜짐");
      servo.write(90);  //문 열림 (서보모터)
      //delay(2000);
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.write("DOOR OPEN");
      digitalWrite(greenLED, HIGH);  //깜
      digitalWrite(redLED, LOW);
      delay(2000);
      digitalWrite(greenLED, LOW);  //빡
      delay(2000);
      digitalWrite(greenLED, HIGH); //깜
      delay(2000);
      digitalWrite(greenLED, LOW); //빡
      delay(2000);
      servo.write(180);   // 문 닫힘 (서보모터)
      lcd.clear();       //lcd reset
      lcd.setCursor(0,0);   
      lcd.write("This is ");
      lcd.setCursor(0,1);
      lcd.write("DOOR OPEN system");
    }
    else if(cmd == 'f'){
      Serial.println("아두이노: 꺼짐");
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.write("DOOR CLOSE");
      digitalWrite(greenLED, LOW);
      digitalWrite(redLED, HIGH);   //깜
      delay(2000);
      digitalWrite(redLED, LOW);     //빡
      delay(2000);
      digitalWrite(redLED, HIGH);     //깜 
      delay(2000);
      digitalWrite(redLED, LOW);      //빡
      delay(2000);
      lcd.clear();   //lcd reset
      lcd.setCursor(0,0);   
      lcd.write("This is ");
      lcd.setCursor(0,1);
      lcd.write("DOOR OPEN system");
    }
  }
}
