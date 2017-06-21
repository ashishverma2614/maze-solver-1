/* libs */
#include <AFMotor.h>
#include <Wire.h>
#include <SoftwareSerial.h>
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
SoftwareSerial Genotronex(2, 4); // RX, TX


/* init */
int BluetoothData;
int stat = 1;
bool track = false;

void setup() {
  Genotronex.begin(9600);
  Serial.begin(9600);

  pinMode(5, INPUT);
  pinMode(6, INPUT);
  pinMode(10, INPUT);
  pinMode(13, INPUT);

  motor1.setSpeed(75);
  motor2.setSpeed(75);
}

//define line follower
void kiri() {
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
}
void kanan() {
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
}
void maju() {
  motor1.run(FORWARD);
  motor2.run(FORWARD);
}
void berhenti() {
  motor1.run(RELEASE);
  motor2.run(RELEASE);
}

//func line follower
void keepontrack() {
  if (track == true) {
    if ((digitalRead(6)) && (digitalRead(5))) {
      berhenti();
    }
    if (!(digitalRead(6)) && (digitalRead(5))) {
      kanan();
    }
    if ((digitalRead(6)) && (!digitalRead(5))) {
      kiri();
    }
    if (!(digitalRead(6)) && (!digitalRead(5))) {
      maju();
    }
  }
  else {
    berhenti();
  }
}

//define belok
void belokkiri() {
  maju();
  delay(150);
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
  delay(1000);
  berhenti();
  delay(200);
}
void belokkanan() {
  maju();
  delay(150);
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  delay(1000);
  berhenti();
  delay(200);
}

void loop() {
  if (Genotronex.available()) {
    BluetoothData = Genotronex.read();
    if (BluetoothData == '1') {
      track = true;
      Genotronex.println("Data Kiri Diterima");
      while (track == true) {
        keepontrack();
        if (!(digitalRead(13))) {
          track = false;
          Genotronex.println("Belok Kiri");
          belokkiri();
        }
        else berhenti();
      }
    }

    if (BluetoothData == '2') {
      keepontrack();
      track = true;
      Genotronex.println("Data Kanan Diterima");
      while (track == true) {
        keepontrack();
        if (!(digitalRead(10))) {
          track = false;
          Genotronex.println("Belok Kanan");
          belokkanan();
        }
        else berhenti();
      }
    }
  }

  else {
    berhenti();
  }
}


