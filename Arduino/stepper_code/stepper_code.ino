#include <SPI.h>
#include <AMIS30543.h>
#include <AccelStepper.h>

//Define Global Input Variable
word input = 0; // Input
word arrival = 0; //Have we sent the arrival message?

//Define Speed and Acceleration Variable
float max_speed = 2000000.0;
float max_acceleration = 500.0;

//Define Stepper Variables
const uint8_t amisDirPin = 2;
const uint8_t amisStepPin = 3;
const uint8_t amisSlaveSelect = 4;

//Initialize (Pololu AMIS 30543 Library) stepper
AMIS30543 stepper;

//Initialize (Accelstepper Library) accelStepper
AccelStepper accelStepper(AccelStepper::DRIVER, amisStepPin, amisDirPin); // Forward

void send_output(word x) {
  // Generate and Write output
  // Communicates in array of format [0xAA,LSByte,MSByte,OxFF]
  // Sends the current value of the output global variable
  byte rawoutput[4];
  rawoutput[0] = 170;
  rawoutput[1] = x;
  rawoutput[2] = x >> 8;
  rawoutput[3] = 255;
  Serial.write(rawoutput, 4);
}

void get_input() {
  //Get input, check for sanity
  //Communicates in array of format [0xAA,LSByte,MSByte,OxFF]
  //Updates the value of the input global variable
  byte rawinput[4];
  if (Serial.available() > 0) {
    Serial.readBytes(rawinput, 4);
  }
  if (rawinput[0] == 170 && rawinput[3] == 255) {
    input = rawinput[1] | rawinput[2] << 8;
    arrival = 0; // when we receive a correctly formatted message send - reset the arrival message tracker
    stepper.enableDriver(); //turn on the driver when we receive a message
  }
}

void setup() {
  //Begin Serial and SPI
  Serial.begin(230400);
  SPI.begin();

  //Set up Steppers
  stepper.init(amisSlaveSelect);
  delay(5);

  //Configure the Steppers
  stepper.resetSettings();
  stepper.setCurrentMilliamps(1700);
  stepper.setStepMode(32);
  stepper.enableDriver();
  delay(5);

  // Maximum Speed and Acceleration
  accelStepper.setMaxSpeed(max_speed);
  accelStepper.setAcceleration(max_acceleration);
}

void loop() {
  //RUN SERIAL IO
  get_input();

  //Run the stepper
  accelStepper.run(); // run stepper

  //Move the Stepper
  //Stage is 20 steps/10 mils
  long destination = 0;
  if (input >= 0 && input <= 10000) { //Range Between 0x0000 and 0x2710
    destination = (input * 64L);
    accelStepper.moveTo(destination); 
  }
  else if (input == 0xFF01) { // 0xFF01 - Homing Op Code, Blocking
    accelStepper.moveTo(-64000 * 5);
    while (abs(accelStepper.distanceToGo()) > 0) {
      accelStepper.run();
    }
    accelStepper.setCurrentPosition(0); //Reset the position variable
    input = 0x0000; // Reset input
  }
  if ((abs(accelStepper.distanceToGo()) == 0) && (arrival == 0)) {
    send_output(0xFF00); // send arrival opcode
    //stepper.disableDriver(); //disable the driver when we have arrived
    arrival = 1;
  }
  /*
    List of op codes :
    Go to position X - 0x0000 - 0x0x2710
    We have arrived at the desired position - 0xFF00
    Home stepper - 0xFF01
  */

}
