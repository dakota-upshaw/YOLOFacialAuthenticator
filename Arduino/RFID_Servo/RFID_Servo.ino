#include <Servo.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN    10
#define RST_PIN   5
#define LED_GOOD   7 //gives output pin for the good LED
#define LED_BAD    8  // Gives output pin for the bad LED
Servo myservo;

MFRC522 rfid(SS_PIN, RST_PIN);
byte authorizedUID[4] = {0x43, 0xBC, 0x86, 0xC9}; //use this to determine what ID's are considered passable

const int buzzer = 4; //buzzer to arduino pin 5

void setup() {
  //myservo.write(0);
  // arduino IO pins/declaration for variables
  myservo.attach(6); //attatches the servo input pin to pin 6
  //pinMode(PR,INPUT);
  pinMode(LED_GOOD, OUTPUT); // used to declare the LED pins as outputs
  pinMode(LED_BAD, OUTPUT);
  pinMode(LED_BAD, OUTPUT);
  // RFID init below
  SPI.begin(); // init SPI bus
  rfid.PCD_Init(); // init MFRC522
  // Serial monitor init below
  Serial.begin(115200); //begins the serial print so we can monitor what section the code is in
  Serial.println("Tap RFID/NFC Tag on reader");
}

void loop() {
  rfid.PCD_Init();
  if (rfid.PICC_IsNewCardPresent()) { // new tag is availabl
    if (rfid.PICC_ReadCardSerial()) { // NUID has been readed
      MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
      // if the tag is authorized
      if (rfid.uid.uidByte[0] == authorizedUID[0] &&
          rfid.uid.uidByte[1] == authorizedUID[1] &&
          rfid.uid.uidByte[2] == authorizedUID[2] &&
          rfid.uid.uidByte[3] == authorizedUID[3] ) {
        Serial.println("Authorized Tag");

        // change angle of servo motor
        cover_PR();

        // control servo motor arccoding to the angle
        
        //Serial.print("Light level: ");
        //Serial.print(light);
      } else {
        Serial.print("Unauthorized Tag with UID:");
        for (int i = 0; i < rfid.uid.size; i++) {
          Serial.print(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
          Serial.print(rfid.uid.uidByte[i], HEX);
        }
        Serial.println();
        stopthat();
        digitalWrite(RST_PIN, HIGH);
        MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
      }

      rfid.PICC_HaltA(); // halt PICC
      Serial.println("halt successful");
      rfid.PCD_StopCrypto1(); // stop encryption on PCD
      Serial.println("stop crypt successful");
    }
  }
}

// RFID=accepted->cover Photoresistor
void cover_PR(){
  myservo.write(60);
  digitalWrite(LED_GOOD, HIGH);
  digitalWrite(LED_BAD, LOW);
  tone(buzzer, 5000); // Send 5KHz sound signal...
  delay(500);        // ...for 1sec
  noTone(buzzer);     // Stop sound...
  delay(500);        // ...for 1sec
}
void stopthat(){
  digitalWrite(LED_GOOD, LOW);
  digitalWrite(LED_BAD, HIGH);
  tone(buzzer, 5000); // Send 5KHz sound signal...
  delay(200);        // ...for 1sec
  noTone(buzzer);     // Stop sound...
  delay(100);        // ...for 1sec
  tone(buzzer, 5000); // Send 5KHz sound signal...
  delay(200);        // ...for 1sec
  noTone(buzzer);     // Stop sound...
}
