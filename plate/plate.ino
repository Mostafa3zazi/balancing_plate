#include <PID_v1.h>
#include <Servo.h>
Servo servoX;
Servo servoY;
double inputX, inputY, outputX, outputY;

double setPointX=(300/600*90);
double setPointY=(225/450*90) ;


PID myPID(&inputX, &outputX, &setPointX, 1, 0.2, 0.4, DIRECT);
PID myPID2(&inputY, &outputY, &setPointY, 1, 0.3, 0.1, DIRECT);
void setup()
{
Serial.begin(9600);
pinMode(13,OUTPUT); 
servoX.attach(5);
servoY.attach(6);
myPID.SetMode(AUTOMATIC);
myPID2.SetMode(AUTOMATIC);
}

void loop()
{
  if (Serial.available() >= 2){
  inputX = Serial.read();
  inputY = Serial.read();
  
  myPID.Compute();
  myPID2.Compute();
  servoX.write(inputX);
  servoY.write(inputY);
  digitalWrite(13,HIGH);
  delay(inputX*4);
  digitalWrite(13,LOW);
  delay(inputY*4);

  }
}
