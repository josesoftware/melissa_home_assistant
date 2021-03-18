###########################################################
## Servicio que se dedica a traducir voz en texto        ##
##-------------------------------------------------------##
## Basado en el STT PocketSphinx no requiere internet    ##
###########################################################

## Importacion de modulos necesarios
import sys, os, time, json
# from pocketsphinx import LiveSpeech, get_model_path
## Usado por Sphinx
from pocketsphinx.pocketsphinx import *
from pocketsphinx import get_model_path
from sphinxbase.sphinxbase import *
## Usado por Vosk
#import queue
#import sounddevice as sd
import vosk
## Para interactuar con el audio
import pyaudio

## Definición de la clase
class STTService:
	##### Sphinx
	## Servicio Sphinx
	sphinxService = None

	##### Vosk
	## Servicio Vosk
	voskService = None
	## Variables del Servicio STT (Vosk)
	voskModel = None

	## Constantes de PyAudio
	PYAUDIO_CHANNELS = 1
	PYAUDIO_BUFFER = 1024
	PYAUDIO_RATE = 16000 # Hz

	##### Otros
	## Instancia del servicio melissa
	melissa = None

	## Constructor
	def __init__(self, melissaService):
		## Instanciamos el servicio de IoT
		self.melissa = melissaService

	## Método que arranca el LiveSpeech de PocketSphinx
	def start(self):
		############# Sphinx
		## Creamos una configuración para el decodificador Sphinx
		sphinxConfig = Decoder.default_config()
		sphinxConfig.set_string('-hmm', os.path.join(get_model_path(), self.melissa.language["stt_model"]))
		sphinxConfig.set_string('-dict', os.path.join(os.path.dirname(__file__), 'STT_Components/', self.melissa.language["keywords_file"] + '.dict'))
		sphinxConfig.set_string('-kws', os.path.join(os.path.dirname(__file__), 'STT_Components/', self.melissa.language["keywords_file"] + '.list'))
		## Inicializamos el reconocimiento de voz Sphinx
		self.sphinxService = Decoder(sphinxConfig)

		############# Vosk
		## Definimos el modelo de lenguaje para Vosk
		self.voskModel = vosk.Model(os.path.join(os.path.dirname(__file__), 'STT_Components/vosk_models/', self.melissa.language["stt_model"]))
		## Inicializamos el reconocimiento de voz
		self.voskService = vosk.KaldiRecognizer(self.voskModel, self.PYAUDIO_RATE)

		## Mensaje de inicio
		print("Speech recognition starts")

		## Inicializmos un PyAudio
		p = pyaudio.PyAudio()

		## Inicializmos un stream en directo con PyAudio
		stream = p.open(format=pyaudio.paInt16, channels=self.PYAUDIO_CHANNELS, rate=self.PYAUDIO_RATE, input=True, frames_per_buffer=self.PYAUDIO_BUFFER)
		stream.start_stream()

		## Comienza el reconocimiento de WakeWord
		self.sphinxService.start_utt()

		## Bucle infinito controlado
		while True:
			## Recuperamos los datos de audio
			data = stream.read(self.PYAUDIO_BUFFER)

			## Si el servicio no esta despierto
			if not self.melissa.wakeUp:
				## Si se han recogido datos correctamente se envian a sphinx
				if data:
					self.first_level_stt(data)
				else:
					break
			else:
				## Si el servicio estaba despierto procesa el audio en segundo nivel
				self.second_level_stt(data)

	## Método usado por Vosk
	#def vosk_callback(self, indata, frames, time, status):
	#	"""This is called (from a separate thread) for each audio block."""
	#	if status:
	#		print(status, file=sys.stderr)
	#	self.q.put(bytes(indata))

	## Método privado que fija un timeout
	#def set_timeout(self):
	#	return time.time() + self.VOSK_TIMEOUT

	## Método privado que chequea un timeout
	#def check_timeout(self, prevTimeout):
		## Retorna el resultado de la comparativa
	#	return time.time() > prevTimeout

	## Método privado que se dedica a buscar el wakeWord
	def first_level_stt(self, rec):
		## Decodifica el audio
		self.sphinxService.process_raw(rec, False, False)
		
		## Si ha encontrado 
		if self.sphinxService.hyp() != None:
			## Despierta el servicio Melissa
			self.melissa.wake()

			## Reinicia el decoder
			self.sphinxService.end_utt()
			self.sphinxService.start_utt()

	## Método privado que se dedica a procesar texto en segundo nivel
	def second_level_stt(self, rec):
		## Mostramos mensaje de aviso
		print('Second level STT proccessing')

		## Si detecta una frase
		if self.voskService.AcceptWaveform(rec):
			## Recupera el resultado
			detectedWords = json.loads(self.voskService.Result())
			
			## Lo manda al NLU
			self.melissa.nlu.from_stt(detectedWords["text"])

		## Dormimos a la inteligencia artificial
		self.melissa.sleep()
