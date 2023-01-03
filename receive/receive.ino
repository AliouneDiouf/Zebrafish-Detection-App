const int LED_ON = 1;
const int LED_OFF = 2;

void setup() {

  Serial.begin(115200);

  pinMode(LED_BUILTIN, OUTPUT);

}
void loop() {
  if (Serial.available() > 0) {
    // Read in request
    int inByte = Serial.read();

    // Take appropriate action
    switch(inByte) {
      case LED_ON:
        digitalWrite(LED_BUILTIN, HIGH);
        break;
      case LED_OFF:
        digitalWrite(LED_BUILTIN, LOW);
        break;
      
    }
  }

}


