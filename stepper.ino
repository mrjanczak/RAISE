#include <AFMotor.h>


// Adafruit Motor shield library
// copyright Adafruit Industries LLC, 2009
// this code is public domain, enjoy!


// Connect a stepper motor with 48 steps per revolution (7.5 degree)
// to motor port #1 (M1 and M2)
AF_Stepper motor(200, 2);
int potpin = A0;
int val;

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
}


void loop() {
  val = analogRead(potpin);            // reads the value of the potentiometer (value between 0 and 1023)
  val = map(val, 0, 1023, 0, 180);     // scale it for use with the servo (value between 0 and 180)
  Serial.println(val);
  motor.setSpeed(val);  // 10 rpm   
  if (val < 5) {
    motor.release();
  }
  else {
    // motor.step(20, FORWARD, SINGLE);
    motor.step(20, FORWARD, DOUBLE);
    // motor.step(20, FORWARD, MICROSTEP);
    // motor.step(20, FORWARD, INTERLEAVE);
     
  }
  // motor.step(50, BACKWARD, MICROSTEP); 
}
