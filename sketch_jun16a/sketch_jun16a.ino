#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

String candidateName = "HappyDavid";
int nameLength = candidateName.length();
int scrollPosition = 0;
unsigned long lastScrollTime = 0;
int scrollDelay = 500;

void setup() {
  Serial.begin(9600);
  
  pinMode(DHTPIN, INPUT_PULLUP);
  dht.begin();
  
  lcd.init();
  lcd.backlight();
  lcd.clear();
  
  // Show startup message
  lcd.setCursor(0, 0);
  lcd.print("Starting...");
  delay(2000);
}

void loop() {
  float temperature = dht.readTemperature();
  
  if (isnan(temperature)) {
    lcd.setCursor(0, 0);
    lcd.print("Sensor Error   ");
    lcd.setCursor(0, 1);
    lcd.print("Check wiring   ");
    Serial.println("ERROR");
    delay(2000);
    return;
  }
  
  // Display name with scrolling if needed
  lcd.setCursor(0, 0);
  if (nameLength <= 16) {
    lcd.print(candidateName);
    for(int i = nameLength; i < 16; i++) {
      lcd.print(" ");
    }
  } else {
    if (millis() - lastScrollTime > scrollDelay) {
      lastScrollTime = millis();
      scrollPosition++;
      if (scrollPosition > nameLength) {
        scrollPosition = 0;
      }
    }
    
    String displayText = "";
    for(int i = 0; i < 16; i++) {
      int idx = (scrollPosition + i) % nameLength;
      displayText += candidateName[idx];
    }
    lcd.print(displayText);
  }
  
  // Display temperature on second row
  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  lcd.print(temperature, 1);
  lcd.print(" C   ");
  
  // Send to serial for PC
  Serial.println(temperature);
  
  delay(1000);
}