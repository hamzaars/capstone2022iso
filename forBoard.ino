#include <stdio.h>
#include <string.h>
#include <AccelStepper.h>

// set up libraries and data types
String all;

int led = 8;

int M0;
int M1;
int M2;

int stepPin;
int dirPin;

int speedM = 50;

int switch_top;
int switch_bottom;

// Function to move steps in a direction
void moveOneStepF(int M0pin, int M1pin, int M2pin, int rpm){
  AccelStepper stepper = AccelStepper(1,stepPin, dirPin);
  stepper.setMaxSpeed(1000);
  
  //setting up microstepping 
  digitalWrite(M0pin, LOW);
  digitalWrite(M1pin,LOW);
  digitalWrite(M2pin, LOW);

  stepper.setCurrentPosition(0);

  while(stepper.currentPosition() !=200){ // set up right now to move 200 full steps
    stepper.setSpeed(-rpm);
    stepper.runSpeed();
  }
  delay(100);
}

// Function to move steps in the opposite direction
void moveOneStepB(int M0pin, int M1pin, int M2pin, int rpm){
  AccelStepper stepper = AccelStepper(1,stepPin, dirPin);
  stepper.setMaxSpeed(1000);
  
  //setting up microstepping 
  digitalWrite(M0pin, LOW);
  digitalWrite(M1pin,LOW);
  digitalWrite(M2pin, LOW);

  stepper.setCurrentPosition(200); // set up to move 200 steps in the oppostie direction

  while(stepper.currentPosition() !=0){
    stepper.setSpeed(-rpm);
    stepper.runSpeed();
  }
  delay(100);
}

//Function to move motor a fixed number of steps forward (move plunger down)
void motormoving_fixedSteps_forward(char M0pin_state,char M1pin_state,char M2pin_state, int M0pin, int M1pin, int M2pin, char switchpinTop, char switchpinBottom, int stepPin, int dirPin, int rpm , int steps) {  
  AccelStepper stepper = AccelStepper(1,stepPin, dirPin);
  stepper.setMaxSpeed(1000);
  
  //setting up microstepping 
  digitalWrite(M0pin, M0pin_state);
  digitalWrite(M1pin,M1pin_state);
  digitalWrite(M2pin, M2pin_state);
  
  //Set the current position to 0:
  stepper.setCurrentPosition(0);

  //Run the motor 
  while(stepper.currentPosition() != steps){ // move the motor until equal to the input steps
    stepper.setSpeed(rpm);
    stepper.runSpeed();
    if (digitalRead(switchpinTop) == LOW || digitalRead(switchpinBottom) == LOW) { // if the limit switch is pressed
     delay(50);
     do{// move back until not pressed
      stepper.setSpeed(-rpm);
      stepper.runSpeed(); 
     }while( digitalRead(switchpinBottom) == LOW || digitalRead(switchpinTop) == LOW );
     moveOneStepB(M0pin,M1pin,M2pin,rpm); // and then move 200 steps in the opposite direction still to get away from the transistory state
     break;
    }
  }
  delay(100);  
  Serial.println(stepper.currentPosition());
}


//Function to move motor a fixed number of steps backward (move plunger up)
void motormoving_fixedSteps_backward(char M0pin_state,char M1pin_state,char M2pin_state, int M0pin, int M1pin, int M2pin, char switchpinTop, char switchpinBottom, int stepPin, int dirPin, int rpm , int steps) {  
  AccelStepper stepper = AccelStepper(1,stepPin, dirPin);
  stepper.setMaxSpeed(1000);
  
  //setting up microstepping 
  digitalWrite(M0pin, M0pin_state);
  digitalWrite(M1pin,M1pin_state);
  digitalWrite(M2pin, M2pin_state);
  
  //Set the current position to number of steps
  stepper.setCurrentPosition(steps);
 
  //Run the motor 
  while(stepper.currentPosition() != 0){ // move until the number of steps is 0
    stepper.setSpeed(rpm);
    stepper.runSpeed();
    if (digitalRead(switchpinTop) == LOW || digitalRead(switchpinBottom) == LOW) { // if limit switch is pressed
     delay(50);
     do{ // move in the opposite direction until the switch is not pressed
      stepper.setSpeed(-rpm);
      stepper.runSpeed(); 
     }while( digitalRead(switchpinBottom) == LOW || digitalRead(switchpinTop) == LOW );
     moveOneStepF(M0pin,M1pin,M2pin,rpm); // and then move 200 steps more in the opposite direction to get out of the transistory state
     break;
    } 
  }
  delay(100);
  Serial.println(steps-(stepper.currentPosition()));
}



//Function to move motor a until limit switch is pressed
void motormoving_untilswitchpressed(char M0pin_state,char M1pin_state,char M2pin_state, int M0pin, int M1pin, int M2pin, char switchpinTop,char switchpinBottom, int stepPin, int dirPin, int rpm) {  
  AccelStepper stepper = AccelStepper(1,stepPin, dirPin);
  stepper.setMaxSpeed(1000);
  
  //setting up microstepping 
  digitalWrite(M0pin, M0pin_state);
  digitalWrite(M1pin,M1pin_state);
  digitalWrite(M2pin, M2pin_state);

  //Set the current position to 0:
  stepper.setCurrentPosition(0);
 
  //Run the motor 
  while(digitalRead(switchpinBottom) == HIGH && digitalRead(switchpinTop) == HIGH ){ // limit switch not pressed
    stepper.setSpeed(rpm);
    stepper.runSpeed();
    
    if (digitalRead(switchpinBottom) == LOW || digitalRead(switchpinTop) == LOW ) {  // pressed
     delay(50);
     do{
      stepper.setSpeed(-rpm); // move in the opposite direction until not pressed
      stepper.runSpeed();
      delay(50);
     }while( digitalRead(switchpinBottom) == LOW || digitalRead(switchpinTop) == LOW );
     break;
   }
 }
  delay(100);  
}



//Main logic code for  moving the motor
void moveMotor(char motor, int full, int half, int quarter){

// set the speed
  int rpmf = speedM;
  int rpmh = speedM;
  int rpmq = speedM;

  // definition of pins for the correct motor
  if (motor == 'd' || motor == 'c'){ // dispenser
    M0 = 13;
    M1 = 12;
    M2 = 11;
    stepPin = 10;
    dirPin = 9;
    switch_top = 54;
    switch_bottom = 55; 
    if(motor == 'c'){ // opposite, dispenser
      full = full*-1;
      half = half*-1;
      quarter = quarter*-1;
      rpmf = rpmf*-1;
      rpmh = rpmh*-1;
      rpmq = rpmq*-1;
    }
  }else if(motor == 'p' || motor == 'o'){ // puncture
    M0 = 8;
    M1 = 7;
    M2 = 6;
    stepPin = 5;
    dirPin = 4;
    switch_top = 56;
    switch_bottom = 57; 
    if(motor == 'p'){// opposite, puncture
      full = full*-1;
      half = half*-1;
      quarter = quarter*-1;
      rpmf = rpmf*-1;
      rpmh = rpmh*-1;
      rpmq = rpmq*-1;
    }
  }else if(motor == 'r' || motor == 'q'){ // rotary
     if(motor == 'q'){
      full = full*-1;
      half = half*-1;
      quarter = quarter*-1;
      rpmf = rpmf*-1;
      rpmh = rpmh*-1;
      rpmq = rpmq*-1;
    }
  }else if (motor == 'x' || motor == 'y'){ // move all the way down/up
    M0 = 13;
    M1 = 12;
    M2 = 11;
    stepPin = 10;
    dirPin = 9;
    switch_top = 54;
    switch_bottom = 55; 
    
    full = 0;
    half = 0;
    quarter = 0;
    if(motor == 'y'){
      rpmf = rpmf*-1;
    }
  }

  // move motor for the amount needed, stop if a switch is triggered
  if (full>0){ // full steps
  Serial.print("full Forward: ");
  motormoving_fixedSteps_forward(LOW,LOW,LOW,M0, M1,M2,
                         switch_top, switch_bottom, stepPin, dirPin,
                         rpmf, full);                        
  }
  if (full<0){ // full steps
  Serial.print("full Backward: "); 
  motormoving_fixedSteps_backward(LOW,LOW,LOW,M0, M1,M2,
                         switch_top, switch_bottom, stepPin, dirPin,
                         rpmf, full*-1);                     
  }
  if (half>0){ // half steps
  Serial.print("half Forward: "); 
  motormoving_fixedSteps_forward(HIGH,LOW,LOW,M0, M1,M2,
                         switch_top, switch_bottom, stepPin, dirPin,
                         rpmh, half);
  }
  if (half<0){ // half steps
  Serial.print("half Backward: ");
  motormoving_fixedSteps_backward(HIGH,LOW,LOW,M0, M1,M2,
                         switch_top, switch_bottom, stepPin, dirPin,
                         rpmh, half*-1);
  }
  if (quarter>0){ // quarter steps
  Serial.print("quarter Forward: ");
  motormoving_fixedSteps_forward(LOW,HIGH,LOW,M0, M1,M2,
                         switch_top, switch_bottom, stepPin, dirPin,
                         rpmq, quarter);   
  }
  if (quarter<0){ // quarter steps
  Serial.print("quarter Backward: ");
  motormoving_fixedSteps_backward(LOW,HIGH,LOW,M0, M1,M2,
                         switch_top, switch_bottom, stepPin, dirPin,
                         rpmq, quarter*-1);
  }

  // to move it back to the limit switches
  if (motor == 'x' || motor == 'y'){
    if (motor == 'x'){
    Serial.println("all the way down full Forward");
    }else if(motor == 'y'){
    Serial.println("all the way down full Backward");
    }
  motormoving_untilswitchpressed(LOW,LOW,LOW,M0, M1,M2,
                         switch_top, switch_bottom, stepPin, dirPin,
                         rpmf);
    if (motor == 'x'){
      moveOneStepB(M0,M1,M2,rpmf);
    }else if(motor == 'y'){
      moveOneStepF(M0,M1,M2,rpmf);
    }
  }
}








void setup(){
  
Serial.begin(9600);  

// set up pull up resistors and input pins
pinMode(M0, INPUT);
pinMode(M1, INPUT);
pinMode(M2, INPUT);
pinMode(A0, INPUT_PULLUP);
pinMode(A1, INPUT_PULLUP);
pinMode(A2, INPUT_PULLUP);
pinMode(A3, INPUT_PULLUP);

}


void loop(){

Serial.flush(); // flush the serial port; takes this away if multiple data coming in

while (Serial.available()==0){} // wait until a response is received from Python

  all = Serial.readStringUntil('k'); // read Python until k

  char motor = all[0]; // 1st character is the motor location

  String fullS;
  String halfS;
  String quarterS;

  // parsing data with ; delimiter
  int k = 2;
  fullS = all[1];
  for(int i = k; all[i] !=';';i++){
    fullS.concat(all[i]);
    k++;
  }
  halfS = all[k+1];
  for(int i = k+2; all[i] !=';';i++){
    halfS.concat(all[i]);
    k++;
  }
  quarterS = all[k+3];
  for(int i = k+4; all[i] !=';';i++){
    quarterS.concat(all[i]);
    k++;
  }

  // converting into integers
  int full = fullS.toInt();
  int half = halfS.toInt();
  int quarter = quarterS.toInt();

  // move motors based on logic sent
  moveMotor(motor, full, half, quarter); // function to move motors

  delay(500);

  
}
