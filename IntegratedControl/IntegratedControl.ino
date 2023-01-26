#include "AltSoftSerial.h"
#include "Adafruit_GFX.h"
#include "Adafruit_SSD1306.h"

// RO to pin 8 & DI to pin 9 when using AltSoftSerial

#define RE 6
#define DE 7

// Pump burst times
#define MOISTURE_DELAY 500
#define N_DELAY 500
#define P_DELAY 500
#define K_DELAY 500

const byte nitro[] = {0x01, 0x03, 0x00, 0x1e, 0x00, 0x01, 0xe4, 0x0c};
const byte phos[] = {0x01, 0x03, 0x00, 0x1f, 0x00, 0x01, 0xb5, 0xcc};
const byte pota[] = {0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xc0};

byte values[11];
AltSoftSerial mod;

// Port definitions
int IN1 = 5;
int IN2 = 2;
int IN3 = 3;
int IN4 = 4;
int Pin1 = A0;
// not sure which analog pins are currently used on the board
int Pin2 = A1;
int Pin3 = A2;
int Pin4 = A3;

// Structure for control parameter
typedef struct param
{
  int value;
  int target;
  int delay;
} Param;

// Structure for ranking priority
typedef struct rank
{
  char first;
  char second;
  char third;
  Param *first_ptr;
  Param *second_ptr;
  Param *third_ptr;
} Rank;

// Global control variables
Param moisture = {0, 0, MOISTURE_DELAY};
Param n = {0, 0, N_DELAY};
Param p = {0, 0, P_DELAY};
Param k = {0, 0, K_DELAY};

// Global variable for priority of each plant nutrient
Rank nutrient_priority = {'N', 'P', 'K', NULL, NULL, NULL};

// Setup code to run once
void setup()
{
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

// Main program loop
void loop()
{
  n.target = 255;
  p.target = 255;
  k.target = 255;
  moisture.target = 430;
  optimize_params();
}

// Nitrogen control algorithm
void n_control()
{
  do
  {
    byte val1;
    val1 = read_nitrogen();
    Serial.print(" = ");
    Serial.print(val1);
    Serial.println(" mg/kg");
    // may need to add a delay here
    // convert the nitrogen reading to an integer
    n.value = int(val1);
    if (n.value >= n.target)
    {
      digitalWrite(IN2, HIGH); // turn pump off
      delay(500);
    }
    else
    {
      digitalWrite(IN2, LOW);  // turn pump on
      delay(n.delay);          // adjust this for dispensing nitrogen fluid
      digitalWrite(IN2, HIGH); // switch pump back off
    }
  } while (n.value < n.target);

  return;
}

// Phosphorous control algorithm
void p_control()
{
  do
  {
    byte val2;
    Serial.print("Phosphorous: ");
    val2 = read_phosphorous();
    Serial.print(" = ");
    Serial.print(val2);
    Serial.println(" mg/kg");
    // may need to add a delay here
    // convert the phosphorous reading to an integer
    p.value = int(val2);
    if (p.value >= p.target)
    {
      digitalWrite(IN3, HIGH); // turn pump off
      delay(500);
    }
    else
    {
      digitalWrite(IN3, LOW);  // turn pump on
      delay(p.delay);          // adjust this for dispensing phosphorous fluid
      digitalWrite(IN3, HIGH); // switch pump back off
    }
  } while (p.value < p.target);

  return;
}

// Potassium control algorithm
void k_control()
{
  do
  {
    byte val3;
    Serial.print("Potassium: ");
    val3 = read_potassium();
    Serial.print(" = ");
    Serial.print(val3);
    Serial.println(" mg/kg");
    // may need to add a delay here
    // convert the potassium reading to an integer
    k.value = int(val3);
    if (k.value >= k.target)
    {
      digitalWrite(IN1, HIGH); // turn pump off
      delay(500);
    }
    else
    {
      digitalWrite(IN1, LOW);  // turn pump on
      delay(k.target);         // adjust this for dispensing potassium fluid
      digitalWrite(IN1, HIGH); // switch pump back off
    }
    delay(5000);
  } while (k.value < k.target);

  return;
}

// Moisture control
void moisture_control()
{
  do
  {
    moisture.value = read_moisture();

    if (moisture.value >= moisture.target)
    {
      digitalWrite(IN2, LOW);  // turn pump for water on
      delay(moisture.delay);   // adjust this delay to control dispensary of water
      digitalWrite(IN2, HIGH); // turn pump for water back off
    }
    else
    {
      digitalWrite(IN2, HIGH); // turn pump for water off
      delay(500);
    }
    Serial.println();
    delay(2000); // not sure if this delay is necessary
  } while (moisture.value >= moisture.target);

  return;
}

// Read nitrogen levels from soil
byte read_nitrogen()
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

// Read phosphorous levels from soil
byte read_phosphorous()
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

// Read potassium levels from soil
byte read_potassium()
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

// Read mpisture levels from soil
int read_moisture()
{
  int moistureVals[5];

  for (int i = 0; i < 5; ++i)
  {
    moistureVals[i] = analogRead(Pin1);
    Serial.println("Moisture level: ");
    Serial.println(moistureVals[i]);
    delay(5000);
  }

  int moistureLvl = compute_modal_moisture(moistureVals, sizeof(moistureVals) / sizeof(moistureVals[0]));

  Serial.println("Modal moisture level: ");
  Serial.println(moistureLvl);

  return moistureLvl;
}

// Read sensor values and activate pumps to optimize soil moisture and NPK
void optimize_params()
{
  byte val;

  val = read_nitrogen();
  n.value = int(val);

  val = read_phosphorous();
  p.value = int(val);

  val = read_potassium();
  k.value = int(val);

  moisture.value = read_moisture();

  if ((moisture.value > moisture.target) && (n.value >= n.target) && (p.value >= p.target) && (k.value >= k.target))
  { // Only moisture condition remains unsatified
    moisture_control();
    delay(500);
  }
  else if ((nutrient_priority.first_ptr->value < nutrient_priority.first_ptr->target) && (moisture.value > moisture.target))
  { // Nitrogen condition not satisfied and plant needs moisture too
    select_controller(nutrient_priority.first);
    delay(500);
  }
  else if ((nutrient_priority.second_ptr->value < nutrient_priority.second_ptr->target) && (moisture.value > moisture.target))
  { // Phosphorous condition not satisfied and plant needs moisture too
    select_controller(nutrient_priority.second);
    delay(500);
  }
  else if ((nutrient_priority.third_ptr->value < nutrient_priority.third_ptr->target) && (moisture.value > moisture.target))
  { // Potassium condition not satisfied and plant needs moisture too
    select_controller(nutrient_priority.third);
    delay(500);
  }
}

// Rank the priority for each element based on how much more of the nutrient needs to be added
// to reach the target. Highest priority assigned to nutrient with biggest offset from target
void compute_nutrient_priority()
{
  int n_offset = n.target - n.value;
  int p_offset = p.target - p.value;
  int k_offset = k.target - k.value;

  if ((n_offset >= p_offset) && (n_offset >= k_offset))
  {
    nutrient_priority.first = 'N';
    nutrient_priority.first_ptr = &n;
    if (p_offset >= k_offset)
    {
      nutrient_priority.second = 'P';
      nutrient_priority.third = 'K';
      nutrient_priority.second_ptr = &p;
      nutrient_priority.third_ptr = &k;
    }
    else
    {
      nutrient_priority.second = 'K';
      nutrient_priority.third = 'P';
      nutrient_priority.second_ptr = &k;
      nutrient_priority.third_ptr = &p;
    }
  }

  else if ((p_offset >= n_offset) && (p_offset >= k_offset))
  {
    nutrient_priority.first = 'P';
    nutrient_priority.first_ptr = &p;
    if (n_offset >= k_offset)
    {
      nutrient_priority.second = 'N';
      nutrient_priority.third = 'K';
      nutrient_priority.second_ptr = &n;
      nutrient_priority.third_ptr = &k;
    }
    else
    {
      nutrient_priority.second = 'K';
      nutrient_priority.third = 'N';
      nutrient_priority.second_ptr = &k;
      nutrient_priority.third_ptr = &n;
    }
  }

  else if ((k_offset >= n_offset) && (k_offset >= p_offset))
  {
    nutrient_priority.first = 'K';
    nutrient_priority.first_ptr = &k;
    if (n_offset >= p_offset)
    {
      nutrient_priority.second = 'N';
      nutrient_priority.third = 'P';
      nutrient_priority.second_ptr = &n;
      nutrient_priority.third_ptr = &p;
    }
    else
    {
      nutrient_priority.second = 'P';
      nutrient_priority.third = 'N';
      nutrient_priority.second_ptr = &p;
      nutrient_priority.third_ptr = &n;
    }
  }
}

// Select which nutrient controller to activate based on the priority level
void select_controller(char priority)
{
  switch (priority)
  {
  case 'N':
    n_control();
    break;

  case 'P':
    p_control();
    break;

  case 'K':
    k_control();
    break;
  }
}

// Return the mode (take smallest value in the event of a tie)
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

    if ((count > maxCount) || (count == maxCount && maxValue > a[i]))
    {
      maxCount = count;
      maxValue = a[i];
    }
  }

  return maxValue;
}

// Round o the nearest 10 for the last five readings from the moisture sensor.
// Return the mode after rounding
int compute_modal_moisture(int a[], int n)
{
  // Round the values for the soil moisture to nearest 10
  for (int i = 0; i < n; ++i)
  {
    double temp = (double)a[i];
    temp = round(temp / 10) * 10;
    a[i] = (int)temp;
  }

  int result = mode(a, sizeof(a) / sizeof(a[0]));

  return result;
}
