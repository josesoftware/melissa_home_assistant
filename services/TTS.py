###################################################################################################################################################
## Este servicio se compone de funciones para la interlocución con lenguajes humanos de forma acústica o lo que es lo mismo TTS (Text to Speech) ##
###################################################################################################################################################

## Importamos librerias
import subprocess
import random
import os

## Clase que representa al objeto
class TTSService:
	#### Atributos
	## Baliza que indica si el TTS esta en uso
	speaking = False

	#### Instancias
	## Instancia del servicio de IoT
	melissa = None

	## Array que componen los mensajes comúnes
	commonMessages = {
		"done_messages": { 
			"ES-ES": ["De acuerdo", "Hecho", "Listo", "Okey", "Vale"], 
			"EN-US": ["I go it", "Done", "Ready", "Okey"] 
			}
	}

	## Constructor
	def __init__(self, iot_service):
		## Fijamos la instancia del modulo LED
		self.melissa = iot_service

	## Método que devuelve un mensaje de audio para indicar que se ha realizado correctamente una opción
	def say_done_message(self):
		## Si no se ha definido un servicio de IoT
		if self.melissa.language is None:
			return

		## Controlamos excepciones
		try:
			## Marcamos la baliza como Speaking
			self.speaking = True

			## Calculamos un indice al azar de mensaje
			message_index = random.randint(0, len(self.commonMessages["done_messages"][self.melissa.language["key"]]) - 1)

			## Leds en modo habla
			if self.melissa.module_led is not None:
				self.melissa.module_led.speak()

			## Lanzamos el TTS con un mensaje de confirmación correcta seleccionado al azar
			process = subprocess.Popen((os.path.dirname(__file__) + '/TTS/speak.sh "{0}" {1}'.format(self.commonMessages["done_messages"][self.melissa.language["key"]][message_index], self.melissa.language["tts_code"])), shell=True, stdout=subprocess.PIPE)
			## Esperamos a que termine
			process.wait()

			## Leds en modo escucha
			if self.melissa.module_led is not None:
				self.melissa.module_led.listen()

			## Modificamos la valiza de uso de servicio
			self.speaking = False
		except:
			## Mostramos mensaje de error
			print("Current language not supported")
			## Modificamos la valiza de uso de servicio
			self.speaking = False
			## Salimos del método
			return

	## Método que devuelve un mensaje de audio para indicar que se ha realizado correctamente una opción
	def say_message(self, message):
		## Si no se ha definido un servicio de IoT
		if self.melissa is None:
			return

		## Controlamos excepciones
		try:
			## Marcamos la baliza como Speaking
			self.speaking = True

			## Leds en modo habla
			if self.melissa.module_led is not None:
				self.melissa.module_led.speak()

			## Lanzamos el TTS con el mensaje pasado por parametro
			process = subprocess.Popen((os.path.dirname(__file__) + '/TTS/speak.sh "{0}" {1}'.format(message, self.melissa.language["tts_code"])), shell=True, stdout=subprocess.PIPE)
			
			## Esperamos a que termine
			process.wait()

			## Leds en modo escucha
			if self.melissa.module_led is not None:
				self.melissa.module_led.listen()

			## Modificamos la valiza de uso de servicio
			self.speaking = False
		except:
			## Mostramos mensaje de error
			print("Current language not supported")
			## Modificamos la valiza de uso de servicio
			self.speaking = False
			## Salimos del método
			return