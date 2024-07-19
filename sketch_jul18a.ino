#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);  // Set the LCD address to 0x27 for a 16 chars and 2 line display

void setup() {
  lcd.init();                      // Initialize the LCD
  lcd.backlight();                 // Turn on the backlight
  Serial.begin(9600);              // Set baud rate to match Python code
}

void loop() {
  if (Serial.available() > 0) {
    int fingerCount = Serial.parseInt();  // Read the finger count from Python
    lcd.clear();                          // Clear the LCD display
    lcd.setCursor(0, 0);                  // Set cursor to the first line
    lcd.print("Finger count:");           // Display the text
    lcd.setCursor(0, 1);                  // Set cursor to the second line
    lcd.print(fingerCount);               // Display the finger count
  }
}
