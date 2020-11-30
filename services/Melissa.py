#################################################################
## Objeto que representa el servicio de IoT 				   ##
#################################################################


## Importamos servicios necesarios
from services.TTS import TTSService
from services.STT import STTService
from services.NLU import NLUService


## Definición de la clase
class MelissaService:
	#### Atributos estaticos
	## Idicador de estado
	WakeUp = False
	## Indicador de bloqueo
	Locked = False
	## Lenguaje de trabajo del servicio
	Language = None

	##### Instancias de módulos
	## Instancia del modulo LED
	LED_Module = None
	## Instancia del modulo de base de datos
	DB_Module = None
	## Instancia del modulo audio
	Audio_Module = None


	##### Instancia de servicios
	TTS = None
	STT = None
	NLU = None

	## Constructor
	def __init__(self, language, LED_Module, DB_Module, Audio_Module):
		############# Instancia de los modulos
		## Definimos el lenguaje de trabajo
		self.Language = language
		## Instanciamos el módulo LED
		self.LED_Module = LED_Module
		## Instanciamos el módulo de base de datos
		self.DB_Module = DB_Module
		## Instanciamos el módulo de audio
		self.Audio_Module = Audio_Module

		############# Instancia del resto de servicios
		## Instanciamos el servicio TTS
		self.TTS = TTSService(self)
		## Instanciamos el servicio STT
		self.STT = STTService(self)
		## Instanciamos el servicio NLU
		self.NLU = NLUService(self)

	## Método que despierta al servicio
	def Wake(self):
		## Modificamos la valiza de estado
		self.WakeUp = True

		## Animamos los led con la animacion de despertar
		if self.LED_Module is not None:
			self.LED_Module.wakeup()

		## Mensaje de aviso
		print("Melissa is wake up")

	## Método que duerme al servicio
	def Sleep(self):
		## Modificamos la valiza de estado
		self.WakeUp = False

		## Apagamos los led
		if self.LED_Module is not None:
			self.LED_Module.off()

		## Mensaje de aviso
		print("Melissa is sleeping")

	## Método que aborta el servicio
	def Abort(self):
		## Modificamos la valiza de estado
		self.WakeUp = False

		## Apagamos los led
		if self.LED_Module is not None:
			self.LED_Module.off()

		## Mensaje de aviso
		print("See you soon!")
		
		## Salimos de la APP
		quit()

	## Método inicia el servicio de IoT
	def StartService(self):
		## Inicia el primer paso del servicio de IoT
		self.STT.Start()

	## Método que recibe datos del servicio STT
	def FromSTT(self, hypothesis):
		## Envia la hipótesis del STT al NLU
		self.NLU.FromSTT(hypothesis)

	## Método que recibe datos del servicio NLU
	def FromNLU(self, intent):
		pass