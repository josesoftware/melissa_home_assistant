# coding=utf-8

##################################
### Importaciones 		 #########
##################################
## Importamos diccionarios
from dictionaries.dictionary import LANGUAGE_DICTIONARY as LANGUAGES

## Importamos módulos
import os
import threading
from pocketsphinx import LiveSpeech, get_model_path
# from modules.led_module import Pixels
from modules.speak_module import *
from modules.device_module import *

## Importacion de objetos
from objects.Service import MelissaService



############################################
## Configuramos Aplicación	  ##############
############################################
## Config general
app_language =  LANGUAGES["ES-ES"]

## Config del STT
stt_samprate = 96000
stt_buffer = 1024
stt_kws_path = os.path.join(os.path.dirname(__file__), 'modules/stt_module/', app_language["keywords_file"] + '.list')
stt_dict_path = os.path.join(os.path.dirname(__file__), 'modules/stt_module/', app_language["keywords_file"] + '.dict')
stt_hmm_path = os.path.join(get_model_path(), app_language["stt_model"])
############################################



#############################################
##	Instanciamos Módulos				   ##
#############################################
## Instanciamos el modulo controlador de los LED
LED_Module = None # Pixels()
## Instanciamos el Text To Speech
TTS = Speak_Module(LED_Module, app_language)
## Instanciamos el Speech To Text
STT = LiveSpeech(
	lm = False,
	verbose = True,
	sampling_rate = stt_samprate,
	buffer_size = stt_buffer,
	no_search = False,
	full_utt = False,
	hmm = stt_hmm_path,
	#lm = os.path.join(model_path, 'es-20k.lm.bin'), ## Para detectar todo tipo de palabras en castellano
	kws = stt_kws_path,
	dict = stt_dict_path
)
## Instanciamos el servicio Melissa
Service = MelissaService(LED_Module)



############################################
## Inicio de aplicación		  			  ##
############################################
print("Speech recognition starts")

## Recorremos las frases que detecta el sistema LiveSpeech
for phrase in STT:
	## Si Melissa está hablando
	if TTS.Speaking == True:
		## Mostramos mensaje
		print("Melissa is speaking, ignoring commands...")

		## Saltamos el ciclo para ignorar comandos generados por error
		continue

	# Recuperamos la posible frase recogida por el STT
	liveText = phrase.hypothesis()
	print(liveText)

	# Si la palabra no es "melissa" y no esta levantado el servicio pasamos de ciclo
	if 'melissa' not in liveText and Service.WakeUp == False:
		continue

	# Si la frase es la palabra clave
	if 'melissa' in liveText and Service.WakeUp == False:
		## Entramos en modo despertar
		Service.Wake()

		## Pasamos de ciclo
		continue

	###################################################################
	###################################################################
	# TEST
	if 'luz' in liveText and 'azul' in liveText:
		## Fijamos el color a los led
		if LED_Module is not None:
			LED_Module.SetRingColorRGB(0, 0, 255)

		## Mensaje de aviso por audio
		TTS.SayDoneMessage()

		## Mensaje de aviso por texto
		print("Done!")

		## Pasamos de ciclo
		continue

	# TEST 2
	if 'descansa' in liveText:
		## Damos orden de abortar
		Service.Abort()

	# TEST 3
	if 'enciende' in liveText and 'rele' in liveText:
		## Fijamos el color a los led
		if LED_Module is not None:
			LED_Module.think()

		## Creamos un objeto temporal
		obj = IoTDevice('10.0.10.218')
		obj.TurnON()

		## Mensaje de aviso por audio
		thread = threading.Thread(target=TTS.SayDoneMessage, name="Speaker", args=[])
		thread.start()

		## Mensaje de aviso por texto
		print("Done!")

		## Pasamos de ciclo
		continue

	# TEST 4
	if 'apaga' in liveText and 'rele' in liveText:
		## Fijamos el color a los led
		if LED_Module is not None:
			LED_Module.think()

		## Creamos un objeto temporal
		obj = IoTDevice('10.0.10.218')
		obj.TurnOFF()

		## Mensaje de aviso por audio
		thread = threading.Thread(target=TTS.SayDoneMessage, name="Speaker", args=[])
		thread.start()

		## Mensaje de aviso por texto
		print("Done!")

		## Pasamos de ciclo
		continue

	# TEST 5
	if 'que' in liveText and 'eres' in liveText:
		## Fijamos el color a los led
		if LED_Module is not None:
			LED_Module.think()

		## Mensaje de aviso por audio
		# TTS.SayMessage("Aún no soy nada, en el futuro pretenden que sea un asistente de hogar y estaré encantada de ayudarte en tu vida diaria")
		arguments = ["Aún no soy nada, en el futuro pretenden que sea un asistente de hogar y estaré encantada de ayudarte en tu vida diaria"]
		thread = threading.Thread(target=TTS.SayMessage, name="Speaker", args=arguments)
		thread.start()

		## Pasamos de ciclo
		continue
	###################################################################
	###################################################################