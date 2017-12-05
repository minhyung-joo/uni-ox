#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT22
#define PPDPIN 8

DHT dht(DHTPIN, DHTTYPE);

unsigned long ppdDuration;
unsigned long ppdStartTime;
unsigned long dhtStartTime;
unsigned long ppdSampleTime = 30000; // 30s
unsigned long dhtSampleTime = 2000;
unsigned long ppdLowPulseOccupancy = 0;
float ppdRatio = 0;
float ppdConcentration = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(PPDPIN, INPUT);
  ppdStartTime = millis();
  dhtStartTime = millis();
}

void loop() {
  ppdDuration = pulseIn(PPDPIN, LOW);
  ppdLowPulseOccupancy = ppdLowPulseOccupancy + ppdDuration;

  if ((millis() - ppdStartTime) > ppdSampleTime) {
    ppdRatio = ppdLowPulseOccupancy/(ppdSampleTime*10.0);
    ppdConcentration = 1.1*pow(ppdRatio, 3) + 520*ppdRatio + 0.62; // use this concentration

    Serial.print("PM:");
    Serial.print(ppdConcentration);
    Serial.print("\n");

    ppdLowPulseOccupancy = 0;
    ppdStartTime = millis();
  }

  if ((millis() - dhtStartTime) > dhtSampleTime) {
    float humidity = dht.readHumidity(); // use this humidity
    float temperature = dht.readTemperature(); // use this temperature

    if (isnan(humidity) || isnan(temperature)) {
      return;
    }

    Serial.print("Temperature:");
    Serial.print(temperature);
    Serial.print("\n");
    Serial.print("Humidity:");
    Serial.print(humidity);
    Serial.print("\n");
    
    dhtStartTime = millis();
  }
}
