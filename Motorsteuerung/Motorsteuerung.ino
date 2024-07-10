// Pin definitions
int MotorA_Enable = 9; // Pwm Pin for motor A
int MotorA_in1 = 8;
int MotorA_in2 = 7;
int MotorB_Enable = 6; // Pwm Pin for motor B
int MotorB_in3 = 5;
int MotorB_in4 = 4;

// Pin definitions for receiving signals
int SpeedPin1 = 2;
int SpeedPin2 = 3;
int DirectionPin1 = 10;
int DirectionPin2 = 11;
int DirectionPin3 = 12;


void setup() {
  // outputs
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(MotorA_Enable, OUTPUT);
  pinMode(MotorA_in1, OUTPUT);
  pinMode(MotorA_in2, OUTPUT);
  pinMode(MotorB_Enable, OUTPUT);
  pinMode(MotorB_in3, OUTPUT);
  pinMode(MotorB_in4, OUTPUT);
  
  // inputs
  pinMode(SpeedPin1, INPUT);
  pinMode(SpeedPin2, INPUT);
  pinMode(DirectionPin1, INPUT);
  pinMode(DirectionPin2, INPUT);
  pinMode(DirectionPin3, INPUT);
}


// the loop function runs over and over again forever
void loop() {

  int speed = getSpeed();
  int direction = getDirection();
   switch (direction) {
    case 0b000:
      stopMotors();
      break;
    case 0b001:
      driveForward(speed);
      break;
    case 0b010:
      driveBackward(speed);
      break;
    case 0b011:
      turnHardLeft(speed);
      break;
    case 0b100:
      turnHardRight(speed);
      break;
    case 0b101:
      turnSoftLeft(speed);
      break;
    case 0b110:
      turnSoftRight(speed);
      break;
    default:
      stopMotors();
      break;
   }

}

/* Test Funktionen für den Loop:
 driveForward(150); // Fullthrottle
  delay(4000);       // wait for two second

  turnSoftLeft(150);
  delay(4000);

  stopMotors();
  delay(4000);

  turnHardLeft(150);
  delay(4000);

  driveBackward(150);
  delay(4000);

  turnHardRight(150);
  delay(4000);
 
  turnSoftRight(150);
  delay(4000);
  */

// MOTOR A -> left tire, MOTOR B -> right tire

int getSpeed() {
  int speed = 0;
  if (digitalRead(SpeedPin1) == HIGH) speed += 85;
  if (digitalRead(SpeedPin2) == HIGH) speed += 170;
  return speed;
}

int getDirection() {
  int direction = 0;
  if (digitalRead(DirectionPin1) == HIGH) direction += 0b001;
  if (digitalRead(DirectionPin2) == HIGH) direction += 0b010;
  if (digitalRead(DirectionPin3) == HIGH) direction += 0b100;
  return direction;
}


void driveForward(int speed){
  analogWrite(MotorA_Enable, speed);
  digitalWrite(MotorA_in1,HIGH);
  digitalWrite(MotorA_in2,LOW);
  analogWrite(MotorB_Enable, speed);
  digitalWrite(MotorB_in3,HIGH);
  digitalWrite(MotorB_in4,LOW);
}

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
  analogWrite(MotorA_Enable, speed * 0.7); // Reduced speed for left tire for soft turn
  digitalWrite(MotorA_in1, HIGH);
  digitalWrite(MotorA_in2, LOW);
  analogWrite(MotorB_Enable, speed);
  digitalWrite(MotorB_in3, HIGH);
  digitalWrite(MotorB_in4, LOW);
}
  

void turnSoftRight(int speed) {
  analogWrite(MotorA_Enable, speed);
  digitalWrite(MotorA_in1, LOW);
  digitalWrite(MotorA_in2, HIGH);
  analogWrite(MotorB_Enable, speed * 0.7);  // Reduced speed for right tire for soft turn
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
