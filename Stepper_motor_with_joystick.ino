const int X_pin = A0;
const int stepPinMotor1 = 2;   // Step pin for Motor 1
const int dirPinMotor1 = 3;    // Direction pin for Motor 1
const int enablePinMotor1 = 4; // Enable pin for Motor 1

// Define connections for Motor 2
const int stepPinMotor2 = 5;   // Step pin for Motor 2
const int dirPinMotor2 = 6;    // Direction pin for Motor 2
const int enablePinMotor2 = 7; // Enable pin for Motor 

// Define connections for Motor 3
const int stepPinMotor3 = 8;   // Step pin for Motor 3
const int dirPinMotor3 = 9;    // Direction pin for Motor 3
const int enablePinMotor3 = 10; // Enable pin for Motor 3

// Define connections for Motor 4
const int stepPinMotor4 = 11;   // Step pin for Motor 4
const int dirPinMotor4 = 12;    // Direction pin for Motor 4
const int enablePinMotor4 = 13;

void setup() {
  pinMode(stepPinMotor1, OUTPUT);
  pinMode(dirPinMotor1, OUTPUT);
  pinMode(enablePinMotor1, OUTPUT);

  pinMode(stepPinMotor2, OUTPUT);
  pinMode(dirPinMotor2, OUTPUT);
  pinMode(enablePinMotor2, OUTPUT);

  pinMode(stepPinMotor3, OUTPUT);
  pinMode(dirPinMotor3, OUTPUT);
  pinMode(enablePinMotor3, OUTPUT);

  pinMode(stepPinMotor4, OUTPUT);
  pinMode(dirPinMotor4, OUTPUT);
  pinMode(enablePinMotor4, OUTPUT);

  digitalWrite(enablePinMotor1, LOW); // Enable Motor 1
  digitalWrite(enablePinMotor2, LOW); // Enable Motor 2
  digitalWrite(enablePinMotor3, LOW); // Enable Motor 3
  digitalWrite(enablePinMotor4, LOW);
}

void loop() {
int a = analogRead(X_pin);
  if ( a > 520)
  {
    digitalWrite(dirPinMotor1, HIGH); // Change direction for Motor 1 (HIGH or LOW)
  // Control Motor 2
  digitalWrite(dirPinMotor2, HIGH); // Change direction for Motor 1 (HIGH or LOW)
  // Control Motor 3
  digitalWrite(dirPinMotor3, HIGH); // Change direction for Motor 2 (HIGH or LOW)
  // Control Motor 4
  digitalWrite(dirPinMotor4, HIGH); 
   for (int i = 0; i < 2000; i++) { // 2000 steps for a full revolution (adjust as needed)
    digitalWrite(stepPinMotor1, HIGH);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor1, LOW);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor2, HIGH);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor2, LOW);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor3, HIGH);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor3, LOW);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor4, HIGH);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor4, LOW);
    delayMicroseconds(10); // Adjust step duration as needed
  }
  }
  else if (a < 400)
  {
    digitalWrite(dirPinMotor1, LOW); // Change direction for Motor 1 (HIGH or LOW)
  // Control Motor 2
  digitalWrite(dirPinMotor2, LOW); // Change direction for Motor 1 (HIGH or LOW)
  // Control Motor 3
  digitalWrite(dirPinMotor3, LOW); // Change direction for Motor 2 (HIGH or LOW)
  // Control Motor 4
  digitalWrite(dirPinMotor4, LOW); 
  for (int i = 0; i < 2000; i++) { // 2000 steps for a full revolution (adjust as needed)
    digitalWrite(stepPinMotor1, HIGH);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor1, LOW);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor2, HIGH);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor2, LOW);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor3, HIGH);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor3, LOW);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor4, HIGH);
    delayMicroseconds(10); // Adjust step duration as needed
    digitalWrite(stepPinMotor4, LOW);
    delayMicroseconds(10); // Adjust step duration as needed
  }
  }
}
