#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
#from rpi_ws281x import *
#from apa102_pi.driver import apa102
from apa102 import APA102
strip = APA102(12, 10, 11, 8)
#import sys

# Importamos libreria de constantes
#import led_constants


# Configuraciones dinamicas
#R = max(min(int(sys.argv[1]), 255), 0)	# Red channel
#G = max(min(int(sys.argv[2]), 255), 0)	# Green channel
#B = max(min(int(sys.argv[3]), 255), 0)	# Blue channel
#A = max(min(int(sys.argv[4]), 255), 0)	# Alpha channel



# Create NeoPixel object with appropriate configuration.
# strip = Adafruit_NeoPixel(led_constants.LED_COUNT, led_constants.LED_PIN, led_constants.LED_FREQ_HZ, led_constants.LED_DMA, led_constants.LED_INVERT, A, led_constants.LED_CHANNEL)
#strip = apa102.APA102(num_led=12, order='rgb')


# Intialize the library (must be called once before other functions).
# strip.begin()
#strip.clear_strip()

strip.set_pixel(0, 255, 0, 0)  # Red
#strip.set_pixel_rgb(1, 0x00FF00)  # Green
#strip.set_pixel_rgb(2, 0x00FF00)  # Green
#strip.set_pixel_rgb(3, 0x0000FF)  # Blue
#strip.set_pixel_rgb(4, 0x0000FF)  # Blue
#strip.set_pixel_rgb(5, 0x0000FF)  # Blue

strip.show()

#strip.cleanup()

# Recorremos los leds
#for i in range(strip.numPixels()):
	# Fijamos el color
#	strip.setPixelColor(i, Color(R,G,B))

	# Actualizamos el estado del led
#	strip.show()

	# Esperamos si se ha definido un delay
#	time.sleep(0/1000.0)
