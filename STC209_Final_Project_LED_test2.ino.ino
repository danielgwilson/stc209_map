/*#define FASTLED_ESP8266_RAW_PIN_ORDER
#define FASTLED_ESP8266_NODEMCU_PIN_ORDER
#define FASTLED_ESP8266_D1_PIN_ORDER*/

#include "FastLED.h"


// How many leds in your strip?
#define NUM_LEDS 324
#define DATA_PIN 5

#define MAX_TIME 44

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


  FastLED.show();
  //delay(500);
  
}
