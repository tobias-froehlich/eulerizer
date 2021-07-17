
int sensorPin = A0;
int sensorValue = 0;
int newSensorValue = 0;
int old1SensorValue = 0;
int old2SensorValue = 0;
int old3SensorValue = 0;
int old4SensorValue = 0;
int old5SensorValue = 0;

int precision = 3;

int value2 = 836;
int value3 = 843; 
int value4 = 850;
int value5 = 861;
int value6 = 869;

int lastOutput = -1;

int count = 0;

void setup() {
  Serial.begin(9600);
}

int hitValue(int value) {
   if (   (abs(sensorValue - value) <= precision)
       && (abs(old1SensorValue - value) <= precision)
       && (abs(old2SensorValue - value) <= precision)
       && (abs(old3SensorValue - value) > precision)
       && (abs(old4SensorValue - value) > precision)
       && (abs(old5SensorValue - value) > precision) ) {
       return 1;    
   }
   return 0;
}

void loop() {
   newSensorValue = analogRead(sensorPin);
   //Serial.println(newSensorValue);
   if (newSensorValue > 900) {
       newSensorValue = 1000;
   }
   sensorValue = sensorValue*0.5 + newSensorValue*0.5;
   count++;
   if (count == 4) {

   if (hitValue(value2)) {
        if (lastOutput != 2) {
            Serial.print("2");
            lastOutput = 2;
        }
   }
    if (hitValue(value3)) {
        if (lastOutput != 3) {
            Serial.print("3");
            lastOutput = 3;
        }
   }
   if (hitValue(value4)) {
        if (lastOutput != 4) {
            Serial.print("4");
            lastOutput = 4;
        }
   }
   if (hitValue(value5)) {
        if (lastOutput != 5) {
            Serial.print("5");
            lastOutput = 5;
        }
   }
   if (hitValue(value6)) {
        if (lastOutput != 6) {
            Serial.print("6");
            lastOutput = 6;
        }
   }
   
   
   old5SensorValue = old4SensorValue;
   old4SensorValue = old3SensorValue;
   old3SensorValue = old2SensorValue;
   old2SensorValue = old1SensorValue;
   old1SensorValue = sensorValue;
   count = 0;
   }
   delay(1);
}
