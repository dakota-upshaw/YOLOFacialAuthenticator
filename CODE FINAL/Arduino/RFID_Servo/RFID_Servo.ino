#include <Servo.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN    10
#define RST_PIN   5
#define LED_GOOD   7
#define LED_BAD    8
Servo myservo;

MFRC522 rfid(SS_PIN, RST_PIN);
byte authorizedUID[4] = {0x43, 0xBC, 0x86, 0xC9};

const int buzzer = 4;
bool debug = true;  // Set to true for debug mode, false for normal operation

void setup() {
  myservo.attach(6);
  pinMode(LED_GOOD, OUTPUT);
  pinMode(LED_BAD, OUTPUT);
  SPI.begin();
  rfid.PCD_Init();
  Serial.begin(115200);
  Serial.println("RFID SCANNER Ready to receive commands");
}

void loop() {
  if (debug) {
    checkRFID();  // Continuously check RFID in debug mode
    delay(1000);  // Delay to avoid overwhelming the serial output and RFID reader
  } else {
    if (Serial.available() > 0) {
      String command = Serial.readStringUntil('\n');
      if (command == "scan_rfid") {
        checkRFID();
      }
    }
  }
}

void checkRFID() {
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    if (memcmp(rfid.uid.uidByte, authorizedUID, 4) == 0) {
      Serial.println("Authorized Tag");
      cover_PR();
      Serial.println("IR_Activated");
    } else {
      Serial.print("Unauthorized Tag with UID:");
      for (int i = 0; i < rfid.uid.size; i++) {
        Serial.print(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
        Serial.print(rfid.uid.uidByte[i], HEX);
      }
      Serial.println();
      stopthat();
    }
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
  }
}

void cover_PR() {
  myservo.write(60);
  digitalWrite(LED_GOOD, HIGH);
  digitalWrite(LED_BAD, LOW);
  tone(buzzer, 5000); // Send 5KHz sound signal...
  delay(500);          // ...for 1sec
  noTone(buzzer);      // Stop sound...
  delay(500);          // ...for 1sec
}

void stopthat() {
  myservo.write(90);
  digitalWrite(LED_GOOD, LOW);
  digitalWrite(LED_BAD, HIGH);
  tone(buzzer, 5000);
  delay(200);
  noTone(buzzer);
  delay(100);
  tone(buzzer, 5000);
   delay(200);
  noTone(buzzer);
   delay(100);
}
