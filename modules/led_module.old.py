

#################################
##############################################################################
## Este modulo compone métodos para interactuar con los led del dispositivo ##
##############################################################################

##################################
## Requerimientos
import time
from rpi_ws281x import *
from libraries.lib_math import IntClamp

##################################
# Configuración de la tira de LEDS
LED_MODULE_LED_COUNT      = 12      # Número de leds.
LED_MODULE_LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_MODULE_LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_MODULE_LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_MODULE_LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_MODULE_LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

## Definicion de la clase
class LED_Module:

	# Método que cambia de color los led del dispositivo indicando como argumentos los canales Red (R), Green (G), Blue (B), Alpha (A)
	# El argumento Delay define el tiempo en milisegundos que tarda en encender cada uno de los leds
	@staticmethod
	def SetColorRGBA(R=0, G=0, B=0, A=0, Delay=0):
		# Truncamos los valores permitidos
		R = IntClamp(R, 0, 255)	# Red channel
		G = IntClamp(G, 0, 255)	# Green channel
		B = IntClamp(B, 0, 255)	# Blue channel
		A = IntClamp(A, 0, 255)	# Alpha channel
		
		# Creamos un objeto del tipo NeoPixel con la configuración determinada
		strip = Adafruit_NeoPixel(LED_MODULE_LED_COUNT, LED_MODULE_LED_PIN, LED_MODULE_LED_FREQ_HZ, LED_MODULE_LED_DMA, LED_MODULE_LED_INVERT, A, LED_MODULE_LED_CHANNEL)

		# Inicializamos la libreria
		strip.begin()

		# Recorremos los leds
		for i in range(strip.numPixels()):
			# Fijamos el color
			strip.setPixelColor(i, Color(R,G,B))
			
			# Actualizamos el estado del led
			strip.show()
			
			# Esperamos si se ha definido un delay
			time.sleep(Delay/1000.0)
			
	# Método que muestra los led de una tira con los colores del arcoiris 
	@staticmethod
	def RainBow(wait_ms=1, iterations=1, Alpha=255):
		# Creamos un objeto del tipo NeoPixel con la configuración determinada
		strip = Adafruit_NeoPixel(LED_MODULE_LED_COUNT, LED_MODULE_LED_PIN, LED_MODULE_LED_FREQ_HZ, LED_MODULE_LED_DMA, LED_MODULE_LED_INVERT, Alpha, LED_MODULE_LED_CHANNEL)

		# Inicializamos la libreria
		strip.begin()
	
		## Draw rainbow that fades across all pixels at once."""
		for j in range(256*iterations):
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, LED_Module.Wheel((i+j) & 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
	
	# Método que genera posiciones desde 0 a 255 para generar patrones de tonos del color del arcoiris
	@staticmethod
	def Wheel(pos):
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)
