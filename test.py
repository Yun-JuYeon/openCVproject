# include <SoftwareSerial.h>
# include <Servo.h>
Servo
myservo;
int
pos = 0;

int
RX = 7;
int
TX = 9;
SoftwareSerial
bluetooth(TX, RX);

void
setup()
{
    Serial.begin(9600);
bluetooth.begin(9600);
pinMode(2, OUTPUT);
pinMode(3, OUTPUT);
pinMode(4, OUTPUT);
pinMode(5, OUTPUT);
myservo.attach(13);
pinMode(A0, INPUT);
pinMode(A1, INPUT);
}

void
loop()
{
    Serial.println(analogRead(A0));
Serial.println(analogRead(A1));

int
fir = analogRead(A0);
int
tou = analogRead(A1);

if (fir < 25)
{
    bluetooth.write("f");
digitalWrite(2, HIGH);
delay(3000);
digitalWrite(2, LOW);
delay(3000);

}
if (tou < 900){
bluetooth.write("d");
digitalWrite(4, HIGH);
delay(3000);
digitalWrite(4, LOW);
delay(3000);

}
if (bluetooth.available()) {
char mes = (char)bluetooth.read();
if (mes == '1'){
digitalWrite(3, HIGH);
}
else if (mes == '2'){
digitalWrite(3, LOW);
}
else if (mes == '3'){
for (pos = 10; pos <= 120; pos += 1){
myservo.write(pos);
delay(20);
}
}
else if (mes == '4'){
for (pos = 120; pos >= 10; pos -= 1){
myservo.write(pos);
delay(20);
}
}
else if (mes == '5'){
digitalWrite(5, HIGH);
}
else if (mes == '6'){
digitalWrite(5, LOW);
}

}
if (bluetooth.available()) {
Serial.write(bluetooth.read());
}
if (Serial.available()) {
bluetooth.write(Serial.read());
}
}