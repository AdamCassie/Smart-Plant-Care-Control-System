#include "AltSoftSerial.h"
#include "Adafruit_GFX.h"
#include "Adafruit_SSD1306.h"

// RO to pin 8 & DI to pin 9 when using AltSoftSerial

#define RE 6
#define DE 7

const byte nitro[] = {0x01, 0x03, 0x00, 0x1e, 0x00, 0x01, 0xe4, 0x0c};
const byte phos[] = {0x01, 0x03, 0x00, 0x1f, 0x00, 0x01, 0xb5, 0xcc};
const byte pota[] = {0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xc0};

byte values[11];
AltSoftSerial mod;

int IN1 = 5;
int IN2 = 2;
int IN3 = 3;
int IN4 = 4;
int Pin1 = A0;
// not sure which analog pins are currently used on the board
int Pin2 = A1;
int Pin3 = A2;
int Pin4 = A3;
float moistureLvl = 0;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(4800);
  mod.begin(4800);

  pinMode(RE, OUTPUT);
  pinMode(DE, OUTPUT);
  // put RS-485 into receive mode
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);

  // Set up pins for moisture control problem
  pinMode(IN1, OUTPUT);
  pinMode(Pin1, INPUT);
  // IN1 in receive mode for relay
  digitalWrite(IN1, HIGH);
  // set up pins for Nitrogen dispensary
  pinMode(IN2, OUTPUT);
  pinMode(Pin2, INPUT);
  // IN2 in receive mode for relay
  digitalWrite(IN2, HIGH);
  // set up pins for Phosphorous dispensary
  pinMode(IN3, OUTPUT);
  pinMode(Pin3, INPUT);
  // IN3 in receive mode for relay
  digitalWrite(IN3, HIGH);
  // set up pins for Potassium dispensary
  pinMode(IN4, OUTPUT);
  pinMode(Pin4, INPUT);
  // IN4 in receive mode for relay
  digitalWrite(IN4, HIGH);
}

void loop()
{
  // nitrogen_control();
  // delay(500);
  // phosphorous_control();
  // delay(500);
  potassium_control();
  delay(500);
  moisture_control();
  delay(500); // can adjust this delay to alter the time cycle for controlling nutrients and moisture
}

// nitrogen control
void nitrogen_control()
{
  int nitrogenLvl = 0;
  do
  {
    byte val1;
    val1 = nitrogen();
    Serial.print(" = ");
    Serial.print(val1);
    Serial.println(" mg/kg");
    // may need to add a delay here
    // convert the nitrogen reading to an integer
    nitrogenLvl = int(val1);
    if (nitrogenLvl >= 210)
    {
      digitalWrite(IN2, HIGH); // turn pump off
      delay(500);
    }
    else
    {
      digitalWrite(IN2, LOW);  // turn pump on
      delay(500);              // adjust this for dispensing nitrogen fluid
      digitalWrite(IN2, HIGH); // switch pump back off
    }
  } while (nitrogenLvl < 210);
  return;
}

// phosphorous control
void phosphorous_control()
{
  int phosphorousLvl = 0;
  do
  {
    byte val2;
    Serial.print("Phosphorous: ");
    val2 = phosphorous();
    Serial.print(" = ");
    Serial.print(val2);
    Serial.println(" mg/kg");
    // may need to add a delay here
    // convert the phosphorous reading to an integer
    phosphorousLvl = int(val2);
    if (phosphorousLvl >= 210)
    {
      digitalWrite(IN3, HIGH); // turn pump off
      delay(500);
    }
    else
    {
      digitalWrite(IN3, LOW);  // turn pump on
      delay(500);              // adjust this for dispensing phosphorous fluid
      digitalWrite(IN3, HIGH); // switch pump back off
    }
  } while (phosphorousLvl < 210);
  return;
}

// potassium control
void potassium_control()
{
  int potassiumLvl = 0;
  do
  {
    byte val3;
    Serial.print("Potassium: ");
    val3 = potassium();
    Serial.print(" = ");
    Serial.print(val3);
    Serial.println(" mg/kg");
    // may need to add a delay here
    // convert the potassium reading to an integer
    potassiumLvl = int(val3);
    if (potassiumLvl >= 220)
    {
      digitalWrite(IN1, HIGH); // turn pump off
      delay(500);
    }
    else
    {
      digitalWrite(IN1, LOW);  // turn pump on
      delay(500);              // adjust this for dispensing potassium fluid
      digitalWrite(IN1, HIGH); // switch pump back off
    }
    delay(5000);
  } while (potassiumLvl < 220);
  return;
}

// moisture control
void moisture_control()
{
  do
  {
    moistureLvl = analogRead(Pin1);
    Serial.println("Moisture level: ");
    Serial.println(moistureLvl);
    if (moistureLvl >= 500)
    {
      digitalWrite(IN2, LOW);  // turn pump for water on
      delay(500);              // adjust this delay to control dispensary of water
      digitalWrite(IN2, HIGH); // turn pump for water back off
    }
    else
    {
      digitalWrite(IN2, HIGH); // turn pump for water off
      delay(500);
    }
    Serial.println();
    delay(2000); // not sure if this delay is necessary
  } while (moistureLvl >= 500);
  return;
}

// read nitrogen levels from soil
byte nitrogen()
{

  mod.flushInput();
  // switch RS-485 to transmit mode
  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);
  delay(100);

  // write out the message
  for (uint8_t i = 0; i < sizeof(nitro); i++)
    mod.write(nitro[i]);

  // wait for the transmission to complete
  mod.flush();

  // switching RS485 to receive mode
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);
  // delay to allow response bytes to be received!
  delay(600);
  // read in the received bytes
  for (byte i = 0; i < 7; i++)
  {
    values[i] = mod.read();
    Serial.print(values[i], HEX);
    Serial.print(' ');
  }
  return values[4];
}

// read phosphorous levels from soil
byte phosphorous()
{
  mod.flushInput();
  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);
  delay(100);
  for (uint8_t i = 0; i < sizeof(phos); i++)
    mod.write(phos[i]);
  mod.flush();
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);
  // delay to allow response bytes to be received!
  delay(600);
  for (byte i = 0; i < 7; i++)
  {
    values[i] = mod.read();
    Serial.print(values[i], HEX);
    Serial.print(' ');
  }
  return values[4];
}

// read potassium levels from soil
byte potassium()
{
  mod.flushInput();
  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);
  delay(100);
  for (uint8_t i = 0; i < sizeof(pota); i++)
    mod.write(pota[i]);
  mod.flush();
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);
  // delay to allow response bytes to be received!
  delay(600);
  for (byte i = 0; i < 7; i++)
  {
    values[i] = mod.read();
    Serial.print(values[i], HEX);
    Serial.print(' ');
  }
  return values[4];
}
