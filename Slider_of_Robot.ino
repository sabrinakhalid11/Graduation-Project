const int stepPinMotor1 = 24;   // Step pin for Motor 1
const int dirPinMotor1 = 25;    // Direction pin for Motor 1
const int enablePinMotor1 = 26; // Enable pin for Motor 1

const int open_PB_1 = 22;
const int close_PB_2 = 23;

void setup() {
  pinMode(stepPinMotor1, OUTPUT);
  pinMode(dirPinMotor1, OUTPUT);
  pinMode(enablePinMotor1, OUTPUT);

  digitalWrite(enablePinMotor1, LOW);

  pinMode(open_PB_1, INPUT_PULLUP);
  pinMode(close_PB_2,INPUT_PULLUP);

  digitalWrite(open_PB_1, HIGH);
  digitalWrite(close_PB_2, HIGH);
}

void loop() {
  if (open_PB_1 == LOW){
    digitalWrite(dirPinMotor1, HIGH); // Change direction for Motor 1 (HIGH or LOW)
  for (int i = 0; i < 2000; i++) { // 2000 steps for a full revolution (adjust as needed)
    digitalWrite(stepPinMotor1, HIGH);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor1, LOW);
  }
  }
  else if (close_PB_2 == LOW){
    digitalWrite(dirPinMotor1, LOW); // Change direction for Motor 1 (HIGH or LOW)
  for (int i = 0; i < 2000; i++) { // 2000 steps for a full revolution (adjust as needed)
    digitalWrite(stepPinMotor1, HIGH);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor1, LOW);
  }
  }
  else {
    digitalWrite(stepPinMotor1, LOW);
  }
}
