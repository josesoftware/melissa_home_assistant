#################################################################################################################################################
## Este módulo se compone de funciones para la interlocución con lenguajes humanos de forma acústica o lo que es lo mismo TTS (Text to Speech) ##
#################################################################################################################################################

## Importamos librerias
import subprocess
import random
import os

## Clase que representa al objeto
class Speak_Module:

	## Instancia del modulo LED
	LED_Module = None

	## Lenguaje de la aplicacion
	app_language = None

	## Baliza que indica si el TTS esta en uso
	Speaking = False

	## Array que componen los mensajes comúnes
	CommonMessages = {
		"done_messages": ["De acuerdo", "Hecho", "Listo", "Okey", "Vale"]
	}

	## Constructor
	def __init__(self, led_module, app_language):
		## Fijamos la instancia del modulo LED
		self.LED_Module = led_module

		## Fijamos el lenguaje de la aplicación
		self.app_language = app_language

	## Método que devuelve un mensaje de audio para indicar que se ha realizado correctamente una opción
	def SayDoneMessage(self):
		## Si no se ha definido un lenguaje salimos del metodo
		if self.app_language is None:
			return

		## Marcamos la baliza como Speaking
		self.Speaking = True

		## Calculamos un indice al azar de mensaje
		message_index = random.randint(0, len(self.CommonMessages["done_messages"]) - 1)

		## Leds en modo habla
		if self.LED_Module is not None:
			self.LED_Module.speak()

		## Lanzamos el TTS con un mensaje de confirmación correcta seleccionado al azar
		process = subprocess.Popen((os.path.dirname(__file__) + '/shell/speak.sh "{0}" {1}'.format(self.CommonMessages["done_messages"][message_index], self.app_language["tts_code"])), shell=True, stdout=subprocess.PIPE)
		
		## Esperamos a que termine
		process.wait()

		## Leds en modo escucha
		if self.LED_Module is not None:
			self.LED_Module.listen()

		## Modificamos la valiza de uso de servicio
		self.Speaking = False

	## Método que devuelve un mensaje de audio para indicar que se ha realizado correctamente una opción
	def SayMessage(self, message):
		## Si no se ha definido un lenguaje salimos del metodo
		if self.app_language is None:
			return

		## Marcamos la baliza como Speaking
		self.Speaking = True

		## Leds en modo habla
		if self.LED_Module is not None:
			self.LED_Module.speak()

		## Lanzamos el TTS con el mensaje pasado por parametro
		process = subprocess.Popen((os.path.dirname(__file__) + '/shell/speak.sh "{0}" {1}'.format(message, self.app_language["tts_code"])), shell=True, stdout=subprocess.PIPE)
		
		## Esperamos a que termine
		process.wait()

		## Leds en modo escucha
		if self.LED_Module is not None:
			self.LED_Module.listen()

		## Modificamos la valiza de uso de servicio
		self.Speaking = False