int value0 = 1;
int value1 = 1;
int value2 = 1;
int value3 = 1;
int value4 = 1;
int value5 = 1;
int value6 = 1;
int value7 = 1;

int oldValue0 = 1;
int oldValue1 = 1;
int oldValue2 = 1;
int oldValue3 = 1;
int oldValue4 = 1;
int oldValue5 = 1;
int oldValue6 = 1;
int oldValue7 = 1;


int oldPedal = -1;
int pedal = 4;


void setup() {
  Serial.begin(9600);

}

void loop() {
  value0 = digitalRead(2);
  value1 = digitalRead(3);
  value2 = digitalRead(4);
  value3 = digitalRead(5);
  value4 = digitalRead(6);
  value5 = digitalRead(7);
  value6 = digitalRead(8);
  value7 = digitalRead(9);

  
  if (value0 == 0 && oldValue0 == 1) {
    pedal = 0;
  }
  if (value1 == 0 && oldValue1 == 1) {
    pedal = 1;
  }
  if (value2 == 0 && oldValue2 == 1) {
    pedal = 2;
  }
  if (value3 == 0 && oldValue3 == 1) {
    pedal = 3;
  }
  if (value4 == 0 && oldValue4 == 1) {
    pedal = 4;
  }
  if (value5 == 0 && oldValue5 == 1) {
    pedal = 5;
  }
  if (value6 == 0 && oldValue6 == 1) {
    pedal = 6;
  }
  if (value7 == 0 && oldValue7 == 1) {
    pedal = 7;
  }

  if (pedal != oldPedal) {
    Serial.print(pedal);
  }

  oldValue0 = value0;
  oldValue1 = value1;
  oldValue2 = value2;
  oldValue3 = value3;
  oldValue4 = value4;
  oldValue5 = value5;
  oldValue6 = value6;
  oldValue7 = value7;
  
  oldPedal = pedal;
  delay(10);
}
