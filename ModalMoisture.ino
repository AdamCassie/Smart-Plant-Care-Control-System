/*
 * https://www.circuitschools.com/
 * Interfacing Soil NPK Sensor with Arduino for measuring
 * Nitrogen, Phosphorus, and Potassium nutrients
 */

#include <math.h>
#include <stdio.h>
#include "AltSoftSerial.h"
#include "Adafruit_GFX.h"
#include "Adafruit_SSD1306.h"

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET -1    // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

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
float moistureLvl = 0;

int moistureVals[5];

void setup()
{
  Serial.begin(4800);
  mod.begin(4800);

  pinMode(RE, OUTPUT);
  pinMode(DE, OUTPUT);

  // put RS-485 into receive mode
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);

  //   // Set up pins for moisture control problem
  pinMode(IN2, OUTPUT);
  pinMode(Pin1, INPUT);

  // IN1 in receive mode for relay
  digitalWrite(IN2, HIGH);
  digitalWrite(IN2, LOW);
}

//   // Set up pins for moisture control problem
//   pinMode(IN1, OUTPUT);
//   pinMode(Pin1, INPUT);

//   // IN1 in receive mode for relay
//   digitalWrite(IN1, LOW);
//   delay(500); // may not be necessary

//   // Set up pins for NPK control problem
//   mod.begin(4800);
//   pinMode(RE, OUTPUT);
//   pinMode(DE, OUTPUT);

//   // put RS-485 into receive mode
//   digitalWrite(DE, LOW);
//   digitalWrite(RE, LOW);
//   delay (1000);

// }

void loop()
{

  byte val1, val2, val3;
  Serial.print("Nitrogen: ");
  val1 = nitrogen();
  Serial.print(" = ");
  Serial.print(val1);
  Serial.println(" mg/kg");
  delay(1000);

  Serial.print("Phosphorous: ");
  val2 = phosphorous();
  Serial.print(" = ");
  Serial.print(val2);
  Serial.println(" mg/kg");
  delay(1000);

  Serial.print("Potassium: ");
  val3 = potassium();
  Serial.print(" = ");
  Serial.print(val3);
  Serial.println(" mg/kg");
  Serial.println();
  Serial.println();

  delay(1000);

  // Start moisture
  for (int i = 0; i < 5; ++i)
  {
    moistureVals[i] = analogRead(Pin1);
    Serial.println("Moisture level: ");
    Serial.println(moistureVals[i]);
    delay(5000);
  }

  moistureLvl = modalMoisture();
  Serial.println("Modal moisture level: ");
  Serial.println(moistureLvl);

  // if (moistureLvl >= 430)
  // {
  //   digitalWrite(IN1, LOW); // turn pump for water on
  //   delay(1000);
  //   digitalWrite(IN1, HIGH); // turn pump for water off
  // }
  // else
  // {
  //   digitalWrite(IN1, HIGH); // turn pump for water off
  //   delay(500);
  // }

  if (val3 < 300)
  {
    digitalWrite(IN1, LOW); // turn pump for water on
    delay(250);
    digitalWrite(IN1, HIGH); // turn pump for water off
  }
  else
  {
    digitalWrite(IN1, HIGH); // turn pump for water off
    delay(500);
  }

  Serial.println();
  // delay(2000);
}

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

// Change this to return the lowest value when there are multiple modes
int mode(int a[], int n)
{
  int maxValue = 0, maxCount = 0, i, j;

  for (i = 0; i < n; ++i)
  {
    int count = 0;

    for (j = 0; j < n; ++j)
    {
      if (a[j] == a[i])
        ++count;
    }

    if (count > maxCount)
    {
      maxCount = count;
      maxValue = a[i];
    }
  }

  return maxValue;
}

int modalMoisture()
{
  // Round the values for the soil moisture to nearest 10
  for (int i = 0; i < 5; ++i)
  {
    double temp = (double)moistureVals[i];
    temp = round(temp / 10) * 10;
    moistureVals[i] = (int)temp;
  }

  int result = mode(moistureVals, sizeof(moistureVals) / sizeof(moistureVals[0]));

  return result;
}
