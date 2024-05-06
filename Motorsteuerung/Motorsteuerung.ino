
int MotorA_Enable = 2;
int MotorA_TR1 = 3;
int MotorA_TR2 = 4;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(MotorA_Enable, OUTPUT);
  pinMode(MotorA_TR1, OUTPUT);
  pinMode(MotorA_TR2, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  forward(2000);
  delay(2000);                       // wait for a second
}

void forward(int timer){
  digitalWrite(MotorA_Enable, HIGH);
  digitalWrite(MotorA_TR1,LOW);
  digitalWrite(MotorA_TR2,HIGH);
  delay(timer);
  digitalWrite(MotorA_Enable, LOW);
  digitalWrite(MotorA_TR1,LOW);
  digitalWrite(MotorA_TR2,LOW);
}

void Turn_Hard_left(){
  // Motor A -> LINKS, Motor B -> Rechts
  MotorA_Backward();
  MotorB_Forward();
}

void MotorA_Forward(){
  
}

void MotorB_Forward(){
  
}

void MotorA_Backwards(){
  
}

void MotorB_Backwards(){
  
}

void MotorA_Stop(){
  
}

void MotorB_Stop(){
  
}
