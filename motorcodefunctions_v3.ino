// final code for DRV8825 motor driver and nema 17 stepper motor with limit switch integated for testing 

#include <AccelStepper.h>
// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver
// Pin layout for punture and dispenser 

#define motorInterfaceType 1 // this applied to all motors 
#define M0_dispenser 13 // dispenser microstepping pin 
#define M1_dispenser 12 // dispenser microstepping pin 
#define M2_dispenser 11 // dispenser microstepping pin 
#define stepPin_dispenser 10 // stepper motor direction 
#define dirPin_dispenser 9 // stepper motor direction

#define M0_puncture 8 // puncture microstepping pin 
#define M1_puncture 7 // puncture microstepping pin 
#define M2_puncture 6 // puncture microstepping pin 
#define stepPin_puncture 5 // puncture stepper motor pin 
#define dirPin_puncture 4 // puncture stepper motor direction

#define switch_dispenser_top A0 // dispenser top limit switch pin 
#define switch_dispenser_bottom A1 // dispenser bottom limit switch pin 
#define switch_puncture_top A2 // puncture top limit switch pin 
#define switch_puncture_bottom A3 // puncture bottom limit switch pin

void setup() {
  Serial.begin(9600);
  // Set the maximum speed in steps per second:
  pinMode(M0_dispenser, INPUT);
  pinMode(M1_dispenser, INPUT);
  pinMode(M2_dispenser, INPUT);
  pinMode(switch_dispenser_top, INPUT_PULLUP);
  pinMode(switch_dispenser_bottom, INPUT_PULLUP);
}

// function that inputs number of steps and microstepping option this will then rotate the motor or untill the switch is pressed **//

void motormoving_fixedSteps(char M0pin_state,char M1pin_state,char M2pin_state, int M0pin, int M1pin, int M2pin, char switchpinTop, char switchpinBottom, int stepPin, int dirPin, int rpm , int steps) {  
  AccelStepper stepper = AccelStepper(1,stepPin, dirPin);
  stepper.setMaxSpeed(1000);
  
  //setting up microstepping 
  digitalWrite(M0pin, M0pin_state);
  digitalWrite(M1pin,M1pin_state);
  digitalWrite(M2pin, M2pin_state);
  
  //Set the current position to 0:
  stepper.setCurrentPosition(0);
 
  //Run the motor 
  while(stepper.currentPosition() != steps && digitalRead(switchpinTop) == HIGH && digitalRead(switchpinBottom) == HIGH){
    stepper.setSpeed(rpm);
    stepper.runSpeed();
    Serial.println(steps);
    if (digitalRead(switchpinTop) == LOW || digitalRead(switchpinBottom) == LOW) {
      break; 
    } 
  }
  delay(100);  
}

void motormoving_untilswitchpressed(char M0pin_state,char M1pin_state,char M2pin_state, int M0pin, int M1pin, int M2pin, char switchpin, int stepPin, int dirPin, int rpm , int steps) {  
  AccelStepper stepper = AccelStepper(1,stepPin, dirPin);
  stepper.setMaxSpeed(1000);
  
  //setting up microstepping 
  digitalWrite(M0pin, M0pin_state);
  digitalWrite(M1pin,M1pin_state);
  digitalWrite(M2pin, M2pin_state);
  
  //Set the current position to 0:
  stepper.setCurrentPosition(0);
 
  //Run the motor 
  while(digitalRead(switchpin) == HIGH){
    stepper.setSpeed(rpm);
    stepper.runSpeed();
    if (digitalRead(switchpin) == LOW) {
      break; 
    } 
  }
  delay(100);  
}

void loop() {
  motormoving_fixedSteps(LOW,LOW,LOW,M0_dispenser, M1_dispenser,M2_dispenser,switch_dispenser_top, switch_dispenser_bottom,stepPin_dispenser, dirPin_dispenser, 100 , 200);
  exit(0); 
}
