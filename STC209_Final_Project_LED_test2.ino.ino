/*#define FASTLED_ESP8266_RAW_PIN_ORDER
#define FASTLED_ESP8266_NODEMCU_PIN_ORDER
#define FASTLED_ESP8266_D1_PIN_ORDER*/

#include "FastLED.h"


// How many leds in your strip?
#define NUM_LEDS 54

// For led chips like Neopixels, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
#define DATA_PIN 5

// Define the array of leds
CRGB leds[NUM_LEDS];

void setup() { 
    Serial.begin(115200);
    FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);
}

int ledxy(int x, int y) {
  // max of 18 x 18
  if (x > 18 || x < 0 || y > 18 || y < 0) {
    //throw Exception();
  }

  if (y % 2 == 0) {
    return y * 18 + x;
  }
  else {
    return y * 18 + (17 - x);
  }
}

void ledon(int x, int y, int red, int gre, int blu) {
  //Serial.println(ledxy(x, y));
  leds[ledxy(x, y)] = CRGB(gre, red, blu);
}

void loop() { 
  // Turn the LED on, then pause
  /*
  leds[0] = CRGB(0, 50, 0);
  leds[1] = CRGB(50, 0, 0);
  leds[2] = CRGB(0, 0, 50);
  leds[3] = CRGB(0, 50, 0);
  leds[4] = CRGB(50, 0, 0);
  leds[5] = CRGB(0, 0, 50);
  leds[10] = CRGB(100, 0, 0);
  
  leds[149] = CRGB(100,0,0);
  */
  ledon(0,0,100,0,0);
  ledon(1,0,100,33,0);
  ledon(2,0,100,66,0);
  ledon(3,0,100,100,0);
  ledon(4,0,100,100,33);
  ledon(5,0,100,100,66);
  ledon(6,0,100,100,100);
  ledon(7,0,100,66,100);
  ledon(8,0,100,33,100);
  ledon(9,0,100,0,100);
  ledon(10,0,66,0,100);
  ledon(11,0,33,0,100);
  ledon(12,0,0,33,100);
  ledon(13,0,0,66,100);
  ledon(14,0,0,100,100);
  ledon(15,0,0,100,66);
  ledon(16,0,0,100,33);

  Serial.println("hi");

  ledon(0,1,100,0,0);
  ledon(1,1,100,33,0);
  ledon(2,1,100,66,0);
  ledon(3,1,100,100,0);
  ledon(4,1,100,100,33);
  ledon(5,1,100,100,66);
  ledon(6,1,100,100,100);
  ledon(7,1,100,66,100);
  ledon(8,1,100,33,100);
  ledon(9,1,100,0,100);
  ledon(10,1,66,0,100);
  ledon(11,1,33,0,100);
  ledon(12,1,0,33,100);
  ledon(13,1,0,66,100);
  ledon(14,1,0,100,100);
  ledon(15,1,0,100,66);
  ledon(16,1,0,100,33);

  Serial.println("hi2");

  ledon(1,2,100,33,0);
  ledon(2,2,100,66,0);
  ledon(3,2,100,100,0);
  ledon(4,2,100,100,33);
  ledon(5,2,100,100,66);
  ledon(6,2,100,100,100);
  ledon(7,2,100,66,100);
  ledon(8,2,100,33,100);
  ledon(9,2,100,0,100);
  ledon(10,2,66,0,100);
  ledon(11,2,33,0,100);
  ledon(12,2,0,33,100);
  ledon(13,2,0,66,100);
  ledon(14,2,0,100,100);
  ledon(15,2,0,100,66);
  ledon(16,2,0,100,33);

  ledon(0,3,100,0,0);
  ledon(1,3,100,0,0);
  ledon(2,3,100,0,0);
  ledon(3,3,100,100,0);
  ledon(4,3,100,100,0);
  ledon(5,3,100,100,0);
  ledon(6,3,100,100,100);
  ledon(7,3,100,0,100);
  ledon(8,3,100,0,100);
  ledon(9,3,100,0,100);
  ledon(10,3,0,0,100);
  ledon(11,3,0,0,100);
  ledon(12,3,0,0,100);
  ledon(13,3,0,0,100);
  ledon(14,3,0,100,100);
  ledon(15,3,0,100,0);
  ledon(16,3,0,100,0);
  
  /*
  leds[0] = CRGB(0, 100, 0);
  leds[4] = CRGB(0, 100, 0);
  leds[18] = CRGB(0, 100, 0);
  leds[19] = CRGB(0, 100, 100);
  */
  FastLED.show();
  delay(500);

  
  // Now turn the LED off, then pause
  leds[0] = CRGB::Black;
  FastLED.show();
  delay(500);
  
}
