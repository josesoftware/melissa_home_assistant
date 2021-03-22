#######################################################################
## Cabecera del paquete de drivers					                 ##
#######################################################################

## Importamos modulos necesarios
from enum import Enum

## Enumeramos los tipos de hardware
class RPIHat(Enum):
	Respeaker2Mic = {"audio-input": 2, "audio-output": 2, "led": 3}
	Respeaker4Mic = {"audio-input": 2, "audio-output": 2, "led": 3}
	Respeaker6Mic = {"audio-input": 2, "audio-output": 2, "led": 3}

class Hardware:
	## Atributos del hardware
	INPUT_AUDIO_CHANNELS = 0
	OUTPUT_AUDIO_CHANNELS = 0
	LED_COUNT = 0

	## Constructor
	def __init__(self, audioIn, audioOut, ledCount):
		## Fijamos los atributos
		self.INPUT_AUDIO_CHANNELS = audioIn
		self.OUTPUT_AUDIO_CHANNELS = audioOut
		self.LED_COUNT = ledCount


	## Método estático que construye un hardware
	@staticmethod
	def Make(hat):
		return RPIHat(hat["audio-input"], hat["audio-output"], hat["led"])