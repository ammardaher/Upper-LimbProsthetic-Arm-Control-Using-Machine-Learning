/*
  EMG-Based Prosthesis Control
  Main Arduino Sketch for Prosthesis Control via EMG Signals
  
  Controls servo motors based on EMG signal classification
  Receives classification commands via Serial from Python
  
  Hardware:
  - Arduino Uno/Mega
  - MYO Armband (via Bluetooth/Serial)
  - 5x Servo Motors (SG90 or equivalent)
  - Power supply for servos
  
  Author: Salman Daher
  License: MIT
*/

#include <Servo.h>

// ============ CONFIGURATION ============
#define SERVO_PIN_THUMB  9
#define SERVO_PIN_INDEX  10
#define SERVO_PIN_MIDDLE 11
#define SERVO_PIN_RING   12
#define SERVO_PIN_PINKY  13

#define BAUD_RATE 9600
#define SERIAL_TIMEOUT 1000  // ms

// Servo angle limits (rest to fully flexed)
#define ANGLE_MIN 0
#define ANGLE_MAX 180

// ============ PINCH MOVEMENTS DEFINITION ============
struct PinchMovement {
  int thumb;
  int index;
  int middle;
  int ring;
  int pinky;
};

const PinchMovement PINCH_POSITIONS[4] = {
  // Pinch 1: Thumb + Index
  {120, 90, 0, 0, 0},
  // Pinch 2: Thumb + Middle
  {130, 0, 90, 0, 0},
  // Pinch 3: Thumb + Ring
  {170, 0, 0, 90, 0},
  // Pinch 4: Thumb + Pinky
  {180, 0, 0, 0, 90}
};

const PinchMovement REST_POSITION = {0, 0, 0, 0, 0};

// ============ SERVO OBJECTS ============
Servo servo_thumb;
Servo servo_index;
Servo servo_middle;
Servo servo_ring;
Servo servo_pinky;

// ============ STATE VARIABLES ============
int current_movement = -1;  // -1 = rest, 0-3 = pinch 1-4
unsigned long last_command_time = 0;
bool debug_mode = true;

// ============ SETUP ============
void setup() {
  // Initialize Serial communication
  Serial.begin(BAUD_RATE);
  Serial.println("EMG Prosthesis Controller - Initializing...");
  
  // Attach servos
  servo_thumb.attach(SERVO_PIN_THUMB);
  servo_index.attach(SERVO_PIN_INDEX);
  servo_middle.attach(SERVO_PIN_MIDDLE);
  servo_ring.attach(SERVO_PIN_RING);
  servo_pinky.attach(SERVO_PIN_PINKY);
  
  // Move to rest position
  move_to_position(REST_POSITION);
  current_movement = -1;
  
  Serial.println("All servos initialized - Ready for commands");
  Serial.println("Commands: 0-3 (pinch 1-4), R (rest), D (debug toggle)");
}

// ============ MAIN LOOP ============
void loop() {
  // Check for incoming serial commands
  if (Serial.available() > 0) {
    char command = Serial.read();
    process_command(command);
    last_command_time = millis();
  }
  
  // Timeout check - return to rest if no command received
  if ((millis() - last_command_time) > SERIAL_TIMEOUT && current_movement != -1) {
    move_to_position(REST_POSITION);
    current_movement = -1;
    if (debug_mode) {
      Serial.println("Timeout - returning to rest position");
    }
  }
  
  delay(10);  // Small delay to prevent overwhelming CPU
}

// ============ COMMAND PROCESSING ============
void process_command(char cmd) {
  switch (cmd) {
    case '0':
    case '1':
    case '2':
    case '3': {
      int movement_id = cmd - '0';
      execute_pinch_movement(movement_id);
      break;
    }
    
    case 'R':
    case 'r': {
      move_to_position(REST_POSITION);
      current_movement = -1;
      if (debug_mode) Serial.println("-> Rest position");
      break;
    }
    
    case 'D':
    case 'd': {
      debug_mode = !debug_mode;
      Serial.print("Debug mode: ");
      Serial.println(debug_mode ? "ON" : "OFF");
      break;
    }
    
    case '\n':
    case '\r':
      // Ignore newlines
      break;
    
    default:
      if (debug_mode) {
        Serial.print("Unknown command: ");
        Serial.println(cmd);
      }
  }
}

// ============ MOVEMENT EXECUTION ============
void execute_pinch_movement(int movement_id) {
  if (movement_id < 0 || movement_id > 3) {
    Serial.println("ERROR: Invalid movement ID");
    return;
  }
  
  if (current_movement == movement_id) {
    return;  // Already in this position
  }
  
  move_to_position(PINCH_POSITIONS[movement_id]);
  current_movement = movement_id;
  
  if (debug_mode) {
    Serial.print("-> Pinch ");
    Serial.print(movement_id + 1);
    Serial.println(" executed");
  }
}

// ============ SERVO CONTROL ============
void move_to_position(const PinchMovement& pos) {
  // Smooth movement using intermediate steps
  const int STEPS = 10;
  const int DELAY_MS = 15;
  
  int current[5] = {
    servo_thumb.read(),
    servo_index.read(),
    servo_middle.read(),
    servo_ring.read(),
    servo_pinky.read()
  };
  
  int target[5] = {pos.thumb, pos.index, pos.middle, pos.ring, pos.pinky};
  
  // Interpolate between current and target positions
  for (int step = 0; step <= STEPS; step++) {
    float progress = (float)step / STEPS;
    
    servo_thumb.write(lerp(current[0], target[0], progress));
    servo_index.write(lerp(current[1], target[1], progress));
    servo_middle.write(lerp(current[2], target[2], progress));
    servo_ring.write(lerp(current[3], target[3], progress));
    servo_pinky.write(lerp(current[4], target[4], progress));
    
    delay(DELAY_MS);
  }
}

// ============ UTILITY FUNCTIONS ============
int lerp(int a, int b, float t) {
  return (int)(a + (b - a) * t);
}

void set_servo_angle(Servo& servo, int angle) {
  angle = constrain(angle, ANGLE_MIN, ANGLE_MAX);
  servo.write(angle);
}

// ============ DIAGNOSTIC FUNCTIONS ============
void print_position() {
  Serial.print("Thumb: ");
  Serial.print(servo_thumb.read());
  Serial.print(" | Index: ");
  Serial.print(servo_index.read());
  Serial.print(" | Middle: ");
  Serial.print(servo_middle.read());
  Serial.print(" | Ring: ");
  Serial.print(servo_ring.read());
  Serial.print(" | Pinky: ");
  Serial.println(servo_pinky.read());
}

void test_servos() {
  Serial.println("Testing all servos...");
  
  for (int i = 0; i < 4; i++) {
    execute_pinch_movement(i);
    delay(500);
  }
  
  move_to_position(REST_POSITION);
  Serial.println("Test complete");
}
