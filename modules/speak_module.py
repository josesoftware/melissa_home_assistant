#################################################################################################################################################
## Este módulo se compone de funciones para la interlocución con lenguajes humanos de forma acústica o lo que es lo mismo TTS (Text to Speech) ##
#################################################################################################################################################

## Importamos librerias
import subprocess
import random
#import festival
import os


## Clase que representa al objeto
class Speak_Module:

	## Variable que contiene el género
	Gender = 'Female'
	LED_Module = None

	## Array que componen los mensajes comúnes
	CommonMessages = {
		"done_messages": ["De acuerdo", "Hecho", "Listo", "Okey", "Vale"]
	}

	## Constructor
	def __init__(self, gender, led_module):

		## Inicializamos festival
		# festival.initialize(1, 210000)

		## Fijamos el género con el que configuramos el TTS
		self.Gender = gender

		## Fijamos la instancia del modulo LED
		self.LED_Module = led_module

	## Método que devuelve un mensaje de audio para indicar que se ha realizado correctamente una opción
	def SayDoneMessage(self):

		## Calculamos un indice al azar de mensaje
		message_index = random.randint(0, len(self.CommonMessages["done_messages"]) - 1)

		## Leds en modo habla
		self.LED_Module.speak()
		print(os.path.dirname(__file__))
		## Lanzamos el TTS con un mensaje de confirmación correcta seleccionado al azar
		#self.assertTrue(festival.sayText(self.CommonMessages["done_messages"][message_index]))
		#stream = os.popen('../speak.sh %s' % self.CommonMessages["done_messages"][message_index])
		#subprocess.run([library_path + 'speak.sh',"'" + self.CommonMessages["done_messages"][message_index] + "'"])
		process = subprocess.Popen((os.path.dirname(__file__)+'/../../speak.sh "%s"' % self.CommonMessages["done_messages"][message_index]), shell=True, stdout=subprocess.PIPE)
		process.wait()

		## Leds en modo habla
		self.LED_Module.listen()

	## Método que devuelve un mensaje de audio para indicar que se ha realizado correctamente una opción
	def SayMessage(self, message):
		## Leds en modo habla
		self.LED_Module.speak()

		## Lanzamos el TTS con un mensaje de confirmación correcta seleccionado al azar
		#self.assertTrue(festival.sayText(self.CommonMessages["done_messages"][message_index]))
		#stream = os.popen('../speak.sh "%s"' % message)
		process = subprocess.Popen((os.path.dirname(__file__)+'/../../speak.sh "%s"' % message), shell=True, stdout=subprocess.PIPE)
		process.wait()
		#subprocess.run([library_path + 'speak.sh',"'" + self.CommonMessages["done_messages"][message_index] + "'"])

		## Leds en modo habla
		self.LED_Module.listen()

		return False
