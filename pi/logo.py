import time
import sys
sys.path.append("/home/pi/rpi_ws281x/python/")
from neopixel import *

# LED Strip configuration
LED_COUNT= 75 # 75 lights in the strip
LED_PIN = 12   # Connected to GPIO pin 2 on pi
LED_FREQ_HZ = 800000 # LED signal frequency should be 800khz
LED_DMA = 5 # ?
LED_INVERT = False

def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
strip.begin()

while True:
    colorWipe(strip, Color(255,0,0))
    colorWipe(strip, Color(0,255,0))
    colorWipe(strip, Color(0,0,255))
    rainbow(strip)
    
        
