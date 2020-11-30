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
	Speaking = False

	#### Instancias
	## Instancia del servicio de IoT
	Melissa = None

	## Array que componen los mensajes comúnes
	CommonMessages = {
		"done_messages": { 
			"ES-ES": ["De acuerdo", "Hecho", "Listo", "Okey", "Vale"], 
			"EN-US": ["I go it", "Done", "Ready", "Okey"] 
			}
	}

	## Constructor
	def __init__(self, iot_service):
		## Fijamos la instancia del modulo LED
		self.Melissa = iot_service

	## Método que devuelve un mensaje de audio para indicar que se ha realizado correctamente una opción
	def SayDoneMessage(self):
		## Si no se ha definido un servicio de IoT
		if self.Melissa.Language is None:
			return

		## Controlamos excepciones
		try:
			## Marcamos la baliza como Speaking
			self.Speaking = True

			## Calculamos un indice al azar de mensaje
			message_index = random.randint(0, len(self.CommonMessages["done_messages"][self.Melissa.Language["key"]]) - 1)

			## Leds en modo habla
			if self.Melissa.LED_Module is not None:
				self.Melissa.LED_Module.speak()

			## Lanzamos el TTS con un mensaje de confirmación correcta seleccionado al azar
			process = subprocess.Popen((os.path.dirname(__file__) + '/TTS/speak.sh "{0}" {1}'.format(self.CommonMessages["done_messages"][self.Melissa.Language["key"]][message_index], self.Melissa.Language["tts_code"])), shell=True, stdout=subprocess.PIPE)
			## Esperamos a que termine
			process.wait()

			## Leds en modo escucha
			if self.Melissa.LED_Module is not None:
				self.Melissa.LED_Module.listen()

			## Modificamos la valiza de uso de servicio
			self.Speaking = False
		except:
			## Mostramos mensaje de error
			print("Current language not supported")
			## Modificamos la valiza de uso de servicio
			self.Speaking = False
			## Salimos del método
			return

	## Método que devuelve un mensaje de audio para indicar que se ha realizado correctamente una opción
	def SayMessage(self, message):
		## Si no se ha definido un servicio de IoT
		if self.Melissa is None:
			return

		## Controlamos excepciones
		try:
			## Marcamos la baliza como Speaking
			self.Speaking = True

			## Leds en modo habla
			if self.Melissa.LED_Module is not None:
				self.Melissa.LED_Module.speak()

			## Lanzamos el TTS con el mensaje pasado por parametro
			process = subprocess.Popen((os.path.dirname(__file__) + '/TTS/speak.sh "{0}" {1}'.format(message, self.Melissa.Language["tts_code"])), shell=True, stdout=subprocess.PIPE)
			
			## Esperamos a que termine
			process.wait()

			## Leds en modo escucha
			if self.Melissa.LED_Module is not None:
				self.Melissa.LED_Module.listen()

			## Modificamos la valiza de uso de servicio
			self.Speaking = False
		except:
			## Mostramos mensaje de error
			print("Current language not supported")
			## Modificamos la valiza de uso de servicio
			self.Speaking = False
			## Salimos del método
			return