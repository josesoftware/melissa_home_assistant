# coding=utf-8

##################################
### Variables de entorno #########
##################################
## Definimos el path de librerias
library_path = "/var/www/html/"

## Importamos librerias
import os
import threading
from pocketsphinx import LiveSpeech, get_model_path
from modules.led_module import Pixels
from modules.speak_module import *
from modules.device_module import *

## Definimos el path de modelos
model_path = get_model_path()


## Definimos el Speech To Text
STT = LiveSpeech(
	lm=False,
	verbose=True,
	sampling_rate=96000,
	buffer_size=1024,
	no_search=False,
	full_utt=False,
	hmm= os.path.join(model_path, 'es-es'),
	#lm= os.path.join(model_path, 'es-20k.lm.bin'),
	kws=os.path.join(os.path.dirname(__file__),'kws.list'), #os.path.join(model_path, 'kws.list'),
	dict=os.path.join(os.path.dirname(__file__), 'test.dict') #os.path.join(model_path, 'es.dict')
)

## Definimos el modulo controlador de los LED
LED_Module = Pixels()

## Definimos el Text To Speech
TTS = Speak_Module("Female", LED_Module)

############################################
## Mensaje de inicio
print("Speech recognition starts")

## Variable que indica si estamos en modo escucha o no
wakeMode = False

## Variable que indica si el sistema esta bloqueado o no
locked = False

speaking = None

## Recorremos las frases que detecta el sistema LiveSpeech
for phrase in STT:
	# Si el speaker se ha definido
	if speaking is not None:
		if speaking.is_alive():
			print("Melissa is speaking, ignoring commands...")
			continue

	# Recuperamos
	liveText = phrase.hypothesis()


	# Si la palabra no es melisa y no esta levantado pasamos de ciclo
	if 'melissa' not in liveText and wakeMode == False:
		continue

	# Si la frase es la palabra clave
	if 'melissa' in liveText and wakeMode == False:
		## Entramos en modo despertar
		wakeMode = True

		## Fijamos el color a los led
		LED_Module.wakeup()

		## Mensaje de aviso
		print("Melissa is wake up")

		## Pasamos de ciclo
		continue

	# TEST
	if 'luz' in liveText and 'azul' in liveText:
		## Fijamos el color a los led
		LED_Module.SetRingColorRGB(0, 0, 255)

		## Mensaje de aviso por audio
		# TTS.SayDoneMessage(LED_Module)

		## Mensaje de aviso por texto
		print("Done!")

		## Pasamos de ciclo
		continue

	# TEST 2
	if 'descansa' in liveText:
		## Fijamos el color a los led
		LED_Module.off()

		## Mensaje de aviso
		print("Bye bye")

		## Salimos de la APP
		quit()

	# TEST 3
	if 'enciende' in liveText and 'rele' in liveText:
		## Fijamos el color a los led
		LED_Module.think()

		## Creamos un objeto temporal
		obj = IoTDevice('10.0.10.218')
		obj.TurnON()

		## Mensaje de aviso por audio
		speaking = threading.Thread(target=TTS.SayDoneMessage, name="Speaker", args=[])
		speaking.start()

		## Mensaje de aviso por texto
		print("Done!")

		## Pasamos de ciclo
		continue

	# TEST 4
	if 'apaga' in liveText and 'rele' in liveText:
		## Fijamos el color a los led
		LED_Module.think()

		## Creamos un objeto temporal
		obj = IoTDevice('10.0.10.218')
		obj.TurnOFF()

		## Mensaje de aviso por audio
		speaking = threading.Thread(target=TTS.SayDoneMessage, name="Speaker", args=[])
		speaking.start()

		## Mensaje de aviso por texto
		print("Done!")

		## Pasamos de ciclo
		continue

	# TEST 5
	if 'que' in liveText and 'eres' in liveText:
		## Fijamos el color a los led
		#LED_Module.think()

		## Mensaje de aviso por audio
		# TTS.SayMessage("Aún no soy nada, en el futuro pretenden que sea un asistente de hogar y estaré encantada de ayudarte en tu vida diaria")
		arguments = ["Aún no soy nada, en el futuro pretenden que sea un asistente de hogar y estaré encantada de ayudarte en tu vida diaria"]
		speaking = threading.Thread(target=TTS.SayMessage, name="Speaker", args=arguments)
		speaking.start()

		## Mensaje de aviso por texto
		# print(locked)

		## Desbloqueamos STT
		# locked = False

		## Pasamos de ciclo
		continue
