int x=0;

void setup() {
 Serial.begin(115200);
 Serial.setTimeout(1); // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
Serial.println(x);
x++;
delay(0.1);
}
