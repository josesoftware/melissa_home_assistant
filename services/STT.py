###########################################################
## Servicio que se dedica a traducir voz en texto        ##
##-------------------------------------------------------##
## Basado en el STT PocketSphinx no requiere internet    ##
###########################################################

## Importacion de modulos necesarios
import os
# from pocketsphinx import LiveSpeech, get_model_path
import queue
import sounddevice as sd
import vosk
import sys
import time
import json

## Definición de la clase
class STTService:
	##### Sphinx
	## Servicio Sphinx
	sphinxService = None

	## Constantes del Servicio STT (Sphinx)
	SPHINX_SAMPLE_RATE = 20000 # Hz
	SPHINX_BUFFER_SIZE = 1024

	##### Vosk
	## Servicio Vosk
	voskService = None
	## Variables del Servicio STT (Vosk)
	voskModel = None
	## Queues que usará el servicio Vosk
	q = queue.Queue()
	## Constantes del Servicio STT (Vosk)
	VOSK_SAMPLE_RATE = 16000 # Hz
	VOSK_BUFFER_SIZE = 8000
	VOSK_INPUT_AUDIO_ID = 0
	VOSK_TIMEOUT = 10

	##### Otros
	## Instancia del servicio melissa
	melissa = None

	## Constructor
	def __init__(self, melissaService):
		## Instanciamos el servicio de IoT
		self.melissa = melissaService

	## Método que arranca el LiveSpeech de PocketSphinx
	def start(self):
		## Definimos el modelo de lenguaje para Vosk
		self.voskModel = vosk.Model(os.path.join(os.path.dirname(__file__), 'STT_Components/vosk_models/', self.melissa.language["stt_model"]))

		## Mensaje de inicio
		print("Speech recognition starts")

		## Lanzamos el STT
		with sd.RawInputStream(samplerate=self.VOSK_SAMPLE_RATE, blocksize=self.VOSK_BUFFER_SIZE, device=self.VOSK_INPUT_AUDIO_ID, dtype='int16', channels=1, callback=self.vosk_callback):
			## Inicializamos el reconocimiento de voz
			rec = vosk.KaldiRecognizer(self.voskModel, self.VOSK_SAMPLE_RATE)

			## Iniciamos primer nivel de reconocimiento de voz
			self.first_level_stt(rec)

		## Recorremos las frases que detecta el sistema LiveSpeech
		# for phrase in self.sphinxService:
			## Si el sistema estaba bloqueado ignorará comandos
			# if self.melissa.wakeUp == True:
				# continue

			## Si el NLU lo autoriza procesamos texto en nivel 2
			# if self.melissa.nlu.match_wake_word(phrase.hypothesis()) == True:
				## Pasamos al nivel 2 de interpretacion
				# self.second_level_stt()

	## Método usado por Vosk
	def vosk_callback(self, indata, frames, time, status):
		"""This is called (from a separate thread) for each audio block."""
		if status:
			print(status, file=sys.stderr)
		self.q.put(bytes(indata))

	## Método privado que fija un timeout
	def set_timeout(self):
		return time.time() + self.VOSK_TIMEOUT

	## Método privado que chequea un timeout
	def check_timeout(self, prevTimeout):
		## Retorna el resultado de la comparativa
		return time.time() > prevTimeout

	## Método privado que se dedica a buscar el wakeWord
	def first_level_stt(self, rec):
		## Mensaje de aviso de inicio del primer nivel del STT
		print ("Waiting a wake word...")
		## Inicializamos el serivio Sphinx
		#self.sphinxService = LiveSpeech(
		# 	lm = False,
		# 	verbose = True,
		# 	sampling_rate = self.SPHINX_SAMPLE_RATE,
		# 	buffer_size = self.SPHINX_BUFFER_SIZE,
		# 	no_search = False,
		# 	full_utt = False,
		# 	hmm = os.path.join(get_model_path(), self.melissa.language["stt_model"]),
		# 	#lm = os.path.join(model_path, 'es-20k.lm.bin'), ## Para detectar todo tipo de palabras en castellano
		# 	kws = os.path.join(os.path.dirname(__file__), 'STT_Components/', self.melissa.language["keywords_file"] + '.list'),
		# 	dict = os.path.join(os.path.dirname(__file__), 'STT_Components/', self.melissa.language["keywords_file"] + '.dict')
		#)

		## Definimos un contador
		counter = 0

		## Bucle infinito controlado
		while True:
			## Recuperamos los datos de audio
			data = self.q.get()

			## Si detecta una frase
			if rec.AcceptWaveform(data):
				## Recupera el resultado
				dataDic = json.loads(rec.Result())

				## Mandamos la frase al NLU
				if self.melissa.nlu.match_wake_word(dataDic["text"]) == True:
					## Pasamos al siguiente nivel de comprension STT
					self.second_level_stt(rec)

			## Incrementamos contador
			counter = counter + 1

			## Si el contador excede el maximo de ciclos purgamos queue
			if counter >= 15:
				self.q.queue.clear()

		## Recorre 
		#for phrase in self.sphinxService:
		#	## Si el sistema estaba bloqueado ignorará comandos
		#	if self.melissa.wakeUp == True:
		#		continue

		#	## Si el NLU lo autoriza procesamos texto en nivel 2
		#	if self.melissa.nlu.match_wake_word(phrase.hypothesis()) == True:
		#		## Sale del bucle
		#		break

		## Anula el reconocimiento Sphinx
		#self.sphinxService = None

		## Pasamos a segundo nivel de comprobación
		#self.second_level_stt(rec)

	## Método privado que se dedica a procesar texto en segundo nivel
	def second_level_stt(self, rec):
		#with sd.RawInputStream(samplerate=self.VOSK_SAMPLE_RATE, blocksize=self.VOSK_BUFFER_SIZE, device=self.VOSK_INPUT_AUDIO_ID, dtype='int16', channels=1, callback=self.vosk_callback):
		## Primero purgamos el queue
		self.q.queue.clear()

		## Mostramos mensaje de aviso
		print('Second level STT proccessing')

		## Inicializamos el reconocimiento de voz en segundo nivel
		#rec = vosk.KaldiRecognizer(self.voskModel, self.VOSK_SAMPLE_RATE)

		## Inicializamos un timeout
		timeout = self.set_timeout()

		## Bucle infinito controlado
		while True:
			## Recuperamos los datos de audio
			data = self.q.get()

			## Si detecta una frase
			if rec.AcceptWaveform(data):
				## Recupera el resultado
				dataDic = json.loads(rec.Result())

				## Mandamos la frase al NLU
				self.melissa.nlu.from_stt(dataDic["text"])

				## Salimos del bucle controlado
				break
			else:
				## Recupera el resultado
				dataWord = json.loads(rec.PartialResult())

				## Si no se ha detectado una frase entera pero detectamos palabras
				if dataWord["partial"] != "":
					## Reseteamos el timeout si se detectan palabras
					self.set_timeout()
			
			## Si se excede el timeout salimos del bucle controlado
			if self.check_timeout(timeout):
				break

		## Dormimos a la inteligencia artificial
		self.melissa.sleep()

		## Purgamos queue
		self.q.queue.clear()