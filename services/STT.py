###########################################################
## Servicio que se dedica a traducir voz en texto        ##
##-------------------------------------------------------##
## Basado en el STT PocketSphinx no requiere internet    ##
###########################################################

## Importacion de modulos necesarios
import sys, os, time, json
## Sphinx
from pocketsphinx.pocketsphinx import *
from pocketsphinx import get_model_path
from sphinxbase.sphinxbase import *
## Vosk
import vosk
## Para multithreading
import threading
import numpy as np

## Definición de la clase
class STTService:
	##### Lista de variables del primer nivel del STT
	FIRST_LVL_STT = {"decoder": [], "thread": [], "result": []}

	##### Lista de variables del segundo nivel del STT
	SECOND_LVL_STT = {"decoder": [], "thread": [], "result": []}

	##### Lista de canales de audio
	audioChannel = list()

	## Instancia del servicio melissa
	melissa = None

	## Constructor
	def __init__(self, melissaService):
		## Instanciamos el servicio de IoT
		self.melissa = melissaService

	## Método que arranca el LiveSpeech de PocketSphinx
	def start(self):
		## Creamos una configuración para el decodificador Sphinx
		sphinxConfig = Decoder.default_config()
		sphinxConfig.set_string('-hmm', os.path.join(get_model_path(), self.melissa.language["stt_model"]))
		sphinxConfig.set_string('-dict', os.path.join(os.path.dirname(__file__), 'STT_Components/', self.melissa.language["keywords_file"] + '.dict'))
		sphinxConfig.set_string('-kws', os.path.join(os.path.dirname(__file__), 'STT_Components/', self.melissa.language["keywords_file"] + '.list'))
		## Definimos el modelo de lenguaje para Vosk
		voskModel = vosk.Model(os.path.join(os.path.dirname(__file__), 'STT_Components/vosk_models/', self.melissa.language["stt_model"]))

		## Inicializamos los componentes del STT
		for i in range(self.melissa.hardware.INPUT_AUDIO_CHANNELS):
			############# Sphinx
			## Configuramos un decoder Sphinx por canal
			decoder = Decoder(sphinxConfig)
			decoder.start_utt()
			self.FIRST_LVL_STT["decoder"].append(decoder)
			self.FIRST_LVL_STT["result"].append(None)
			self.FIRST_LVL_STT["thread"].append(None)

			############# Vosk
			self.SECOND_LVL_STT["decoder"].append(vosk.KaldiRecognizer(voskModel, self.melissa.driver_audio.READ_RATE))
			self.SECOND_LVL_STT["result"].append(None)
			self.SECOND_LVL_STT["thread"].append(None)

		## Mensaje de inicio
		print("Speech recognition starts")

		## Bucle infinito controlado
		while True:
			## Recuperamos los datos de audio
			data = self.melissa.driver_audio.read()

			## Convertimos el string en un numpy Array
			data_array = np.frombuffer(data, dtype='int16')

			## Limpiamos la lista de datos
			self.audioChannel.clear()

			## Por cada canal definido
			for i in range(self.melissa.hardware.INPUT_AUDIO_CHANNELS):
				self.audioChannel.append(data_array[i::self.melissa.hardware.INPUT_AUDIO_CHANNELS])

			## Si el servicio no esta despierto
			if not self.melissa.wakeUp:
				## Purga la lista de procesos del nivel 2
				self.SECOND_LVL_STT["result"] = [None] * self.melissa.hardware.INPUT_AUDIO_CHANNELS

				## Por cada canal de audio procesa un decoder
				for i in range(len(self.audioChannel)):
					#if firstStep["thread"][i] is None:
					t = threading.Thread(target=self.first_level_stt, args=(i, self.audioChannel[i].tobytes()))
					self.FIRST_LVL_STT["thread"][i] = t
					t.start()

				## Espera a que los subprocesos terminen
				for th in self.FIRST_LVL_STT["thread"]:
					th.join()

				## Comprueba la wake word por cada decodificador
				for index in range(len(self.FIRST_LVL_STT["decoder"])):
					if self.FIRST_LVL_STT["decoder"][index].hyp() != None:
						##### DEBUG
						## print ("\nChannel " + str(index + 1) + " - ", [(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in firstStep["decoder"][index].seg()], "\n")
						self.FIRST_LVL_STT["result"][index] = True
						self.FIRST_LVL_STT["decoder"][index].end_utt()
						self.FIRST_LVL_STT["decoder"][index].start_utt()

				## Siempre que todos los STT Lvl 1 hayan contestado
				if None not in self.FIRST_LVL_STT["result"]:
					## Despierta el servicio melissa
					self.melissa.wake()
					## Mensaje debug
					print ("Second level of recognition starting")
			else:
				## Purga la lista de procesos del nivel 1
				self.FIRST_LVL_STT["result"] = [None] * self.melissa.hardware.INPUT_AUDIO_CHANNELS

				## Por cada canal de audio procesa un decoder
				for i in range(len(self.audioChannel)):
					# if secondStep["thread"][i] is None:
					t = threading.Thread(target=self.second_level_stt, args=(i, self.audioChannel[i].tobytes()))
					self.SECOND_LVL_STT["thread"][i] = t
					t.start()

				## Espera a que los subprocesos terminen
				for th in self.SECOND_LVL_STT["thread"]:
					th.join()

				## Siempre que todos los STT Lvl 2 hayan contestado
				if None not in self.SECOND_LVL_STT["result"]:
					## Declaramos un json de retorno
					phraseArray = list()

					## Comprueba si algun decodificador ha encontrado alguna palabra clave
					for result in self.SECOND_LVL_STT["result"]:
						## Recupera el resultado
						detectedWords = json.loads(result)

						## Añadimos el resultado a la lista
						phraseArray.append((detectedWords["text"])

					## Lo manda al NLU
					# self.melissa.nlu.from_stt(phraseArray)
					print("Lvl 2 STT Return: ", phraseArray)

					## Dormimos a la inteligencia artificial
					self.melissa.sleep()

	## Método privado que se dedica a buscar el wakeWord
	def first_level_stt(self, index, data):
		if data:
			self.FIRST_LVL_STT["decoder"][index].process_raw(data, False, False)
		else:
			return

	## Método privado que se dedica a procesar texto en segundo nivel
	def second_level_stt(self, index, data):
		## Si detecta una frase
		if self.SECOND_LVL_STT["decoder"][index].AcceptWaveform(data):
			## Recupera el resultado
			self.SECOND_LVL_STT["result"][index] = self.SECOND_LVL_STT["decoder"][index].Result()