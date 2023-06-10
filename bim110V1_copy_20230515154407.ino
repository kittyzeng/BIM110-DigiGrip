// Arduino as load cell amplifier
// modified from Christian Liljedahl; christian.liljedahl.dk

// ============
// Variables for load cell calibration
// ============

float loadA = 0; // kg CHANGE to known value
int analogvalA = 0; // analog reading taken with load A on the load cell CHANGE

float loadB = 0; // kg CHANGE to known value
int analogvalB = 0; // analog reading taken with load B on the load cell CHANGE

float analogValueAverage = 0;

// How often do we do readings?
long time = 0; //
int timeBetweenReadings = 100; // We want a reading every 100 ms; CHANGE VALUE HERE 

// Debounce function 
// Modified from created 21 Nov 2006
// by David A. Mellis
// modified 30 Aug 2011
// by Limor Fried
// modified 28 Dec 2012
// by Mike Walters
// modified 30 Aug 2016
// by Arturo Guadalupi

// ============
// Variables for button and LED light
// ============

const int LED_PIN = 10; 
const int BUTTON = 3; 

int isCurrentlyRecording = LOW;

int buttonState = HIGH;                
int lastReading = HIGH;      

unsigned long lastDebounceTime = 0;   
unsigned long buttonPressedTime = 0;

unsigned long debounceDelay = 50;     
unsigned long minHoldTime = 3000;

// ============
// Variables for writing recorded data to file
// ============

int currentPatientId = 0;

// ============
// libraries for SD card
// ============

#include <SPI.h>
#include <SD.h>


void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON, INPUT);
  digitalWrite(LED_PIN, isCurrentlyRecording);

  // probably need to call startNewPatient() here
  // or alternatively, have a variable for if we've ever made a measurement or not
  // and when we start a measurement, if it's our first measurement ever (since powering on)
  // then start a new patient at that point
} 

void readButton() {
  int reading = digitalRead(BUTTON);

  if (reading != lastReading) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) { //value is the same which means that the button is at stable value 
    if (reading != buttonState) { // value is stable at something different from the previous state, so we either pressed or stopped pressing
      buttonState = reading;

      if (buttonState == LOW) {
        buttonPressedTime = millis();
      } else {
        if ((millis() - buttonPressedTime) > minHoldTime) {
          // start new patient
          if (!isCurrentlyRecording) {
            startNewPatient();
          }
        } else {
          // start new recording/stop current recording
          toggleRecordingState();
        }
      }
    }
  }

  lastReading = reading;
}

void startNewPatient() {
  Serial.println("Starting new patient");
  
  //patientCount += 1;

  // modify any variables to identify the patient, change patient ID, etc.
  // reset measurement count, etc.
}

void toggleRecordingState() {
  isCurrentlyRecording = !isCurrentlyRecording;
  if (isCurrentlyRecording) {
    Serial.println("Started recording");
    // open file. folder name should contain current time, patient ID
    // file name should just be sequential (add measurementCount variable or smth)
  } else {
    Serial.println("Stopped recording");
    // close file
  }
}

void loop() {
  int analogValue = analogRead(0);

  // running average - We smooth the readings a little bit
  analogValueAverage = 0.99*analogValueAverage + 0.01*analogValue;

  // Is it time to print?
  if(millis() > time + timeBetweenReadings){
    float load = analogToLoad(analogValueAverage);

    //Serial.print("analogValue: ");Serial.println(analogValueAverage);
    //Serial.print("             load: ");Serial.println(load,5);
    time = millis();
  }

  readButton();
}

//CALIBRATING LOAD CELL
float analogToLoad(float analogval){

  // using a custom map-function, because the standard arduino map function only uses int
  float load = mapfloat(analogval, analogvalA, analogvalB, loadA, loadB);
  return load;
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}