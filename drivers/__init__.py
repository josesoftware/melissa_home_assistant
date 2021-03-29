#######################################################################
## Cabecera del paquete de drivers					                 ##
#######################################################################


## Importacion de utilidades
from libraries.lib_utils import replace_char

## Enumeramos los tipos de hardware
class RPIHat:
	## Atributos
	Respeaker2Mic = {"audio-input": 2, "audio-output": 2, "led": 3}
	Respeaker4Mic = {"audio-input": 4, "audio-output": 2, "led": 12}
	Respeaker6Mic = {"audio-input": 6, "audio-output": 2, "led": 12}

## Clase que representa un objeto de tipo hardware, el sistema se basará en el hardware para operar
class Hardware:
	## Atributos constantes del hardware
	INPUT_AUDIO_CHANNELS = 0
	OUTPUT_AUDIO_CHANNELS = 0
	LED_COUNT = 0

	## Atributos dinámicos del hardware
	hostname = "Melissa-Bee"
	alias = "Melissa Bee"
	ipaddress = "127.0.0.1"
	machine = "md5-id"

	## Constructor
	def __init__(self, audioIn, audioOut, ledCount):
		## Fijamos los atributos
		self.INPUT_AUDIO_CHANNELS = audioIn
		self.OUTPUT_AUDIO_CHANNELS = audioOut
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
		return Hardware(hat["audio-input"], hat["audio-output"], hat["led"])