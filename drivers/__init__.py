#######################################################################
## Cabecera del paquete de drivers					                 ##
#######################################################################


## Importacion de utilidades
from libraries.lib_utils import replace_char

## Enumeramos los tipos de hardware
class RPIHat:
	## Atributos
	Respeaker2Mic = {"audio-input": 2, "audio-output": 2, "led": 3, "input-rate": 16000, "input-width": 2, "output-rate": 44100}
	Respeaker4Mic = {"audio-input": 4, "audio-output": 2, "led": 12, "input-rate": 16000, "input-width": 2, "output-rate": 44100}
	Respeaker6Mic = {"audio-input": 8, "audio-output": 2, "led": 12, "input-rate": 16000, "input-width": 2, "output-rate": 44100}

## Clase que representa un objeto de tipo hardware, el sistema se basará en el hardware para operar
class Hardware:
	## Atributos constantes del hardware
	INPUT_AUDIO_CHANNELS = 0
	INPUT_AUDIO_RATE = 0
	INPUT_AUDIO_WIDTH = 0
	OUTPUT_AUDIO_CHANNELS = 0
	LED_COUNT = 0

	## Atributos dinámicos del hardware
	hostname = "Melissa-Bee"
	alias = "Melissa Bee"
	ipaddress = "127.0.0.1"
	machine = "md5-id"

	## Constructor
	def __init__(self, audioIn, audioOut, ledCount, audioInRate, audioInWidth, audioOutRate):
		## Fijamos los atributos
		self.INPUT_AUDIO_CHANNELS = audioIn
		self.INPUT_AUDIO_RATE = audioInRate
		self.INPUT_AUDIO_WIDTH = audioInWidth
		self.OUTPUT_AUDIO_CHANNELS = audioOut
		self.OUTPUT_AUDIO_RATE = audioOutRate
		self.LED_COUNT = ledCount

	## Método que recupera información de la máquina
	def set_hardware_info(self, hostname, machineId):
		## Fija el hostname
		self.hostname = hostname
		self.alias = replace_char(hostname, "-", " ")
		self.machine = machineId

	## Método estático que construye un hardware
	@staticmethod
	def Make(hat):
		return Hardware(hat["audio-input"], hat["audio-output"], hat["led"], hat["input-rate"], hat["input-width"], hat["output-rate"])