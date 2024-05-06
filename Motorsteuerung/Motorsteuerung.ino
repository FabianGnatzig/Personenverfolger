// Pin definitions
int MotorA_Enable = 9; // Pwm Pin for motor A
int MotorA_in1 = 8;
int MotorA_in2 = 7;
int MotorB_Enable = 6; // Pwm Pin for motor B
int MotorB_in3 = 5;
int MotorB_in4 = 4;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(MotorA_Enable, OUTPUT);
  pinMode(MotorA_in1, OUTPUT);
  pinMode(MotorA_in2, OUTPUT);
  pinMode(MotorB_Enable, OUTPUT);
  pinMode(MotorB_in3, OUTPUT);
  pinMode(MotorB_in4, OUTPUT);
}

// serial communication?
// Serial.begin(9600);


// the loop function runs over and over again forever
void loop() {

  driveForward(255); // Fullthrottle
  delay(4000);       // wait for two second

  driveBackward(255);
  delay(4000);

  turnHardLeft(255);
  delay(4000);

  turnHardRight(255);
  delay(4000);

  turnSoftLeft(255);
  delay(4000);

  turnSoftRight(255);
  delay(4000);

  stopMotors();
  delay(4000);

}

// MOTOR A -> left tire, MOTOR B -> right tire

void driveForward(int speed){
  analogWrite(MotorA_Enable, speed);
  digitalWrite(MotorA_in1,HIGH);
  digitalWrite(MotorA_in2,LOW);

  analogWrite(MotorB_Enable, speed);
  digitalWrite(MotorB_in3,HIGH);
  digitalWrite(MotorB_in4,LOW);
}

/*void Turn_Hard_left(){
  // Motor A -> LINKS, Motor B -> Rechts
  MotorA_Backward();
  MotorB_Forward();
}

void Turn_Hard_right(){
MotorA_Forward();
MotorB_Backward();
} */

void driveBackward(int speed){

  analogWrite(MotorA_Enable, speed);
  digitalWrite(MotorA_in1, LOW);
  digitalWrite(MotorA_in2, HIGH);

  analogWrite(MotorB_Enable, speed);
  digitalWrite(MotorB_in3, LOW);
  digitalWrite(MotorB_in4, HIGH);  
}

void turnHardLeft(int speed){

  analogWrite(MotorA_Enable, speed);
  digitalWrite(MotorA_in1, LOW);
  digitalWrite(MotorA_in2, HIGH);
  

  analogWrite(MotorB_Enable, speed);
  digitalWrite(MotorB_in3, HIGH);
  digitalWrite(MotorB_in4, LOW);
}

void turnHardRight(int speed){

  analogWrite(MotorA_Enable, speed);
  digitalWrite(MotorA_in1, HIGH);
  digitalWrite(MotorA_in2, LOW);
  
  analogWrite(MotorB_Enable, speed);
  digitalWrite(MotorB_in3, LOW);
  digitalWrite(MotorB_in4, HIGH);
}

void turnSoftLeft(int speed) {
  analogWrite(MotorA_Enable, speed * 0.8); // Reduced speed for left tire for soft turn
  digitalWrite(MotorA_in1, LOW);
  digitalWrite(MotorA_in2, HIGH);

  analogWrite(MotorB_Enable, speed);
  digitalWrite(MotorB_in3, HIGH);
  digitalWrite(MotorB_in4, LOW);
}
  

  void turnSoftRight(int speed) {
  analogWrite(MotorA_Enable, speed);
  digitalWrite(MotorA_in1, LOW);
  digitalWrite(MotorA_in2, HIGH);

  analogWrite(MotorB_Enable, speed * 0.8);  // Reduced speed for right tire for soft turn
  digitalWrite(MotorB_in3, LOW);
  digitalWrite(MotorB_in4, HIGH);
  }
  

void stopMotors(){

  analogWrite(MotorA_Enable, 0);
  digitalWrite(MotorA_in1, LOW);
  digitalWrite(MotorA_in2, LOW);
  
  analogWrite(MotorB_Enable, 0);
  digitalWrite(MotorB_in3, LOW);
  digitalWrite(MotorB_in4, LOW);
  
  
}

