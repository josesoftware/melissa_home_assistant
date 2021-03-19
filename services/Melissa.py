#################################################################
## Objeto que representa el servicio de IoT 				   ##
#################################################################

## Importacion de modulos
import json

## Importamos servicios necesarios
from services.TTS import TTSService
from services.STT import STTService
from services.NLU import NLUService

## Importamos objetos
from objects.Switch import Switch
from objects.Bolb import Bolb
from objects.Ambience import Ambience


## Definición de la clase
class MelissaService:
	#### Atributos estaticos
	## Idicador de estado
	wakeUp = False
	## Indicador de bloqueo
	locked = False
	## Lenguaje de trabajo del servicio
	language = None

	#### Atributos dinamicos
	## Lista de cosas ( Things )
	things = { 
		"commands": {},
		"ambiences": {},
		"devices": {}
	}

	## Lista de WakeWords
	wakeWords = [
		"melissa"
	]

	##### Instancias de módulos
	## Instancia del modulo LED
	module_led = None
	## Instancia del modulo de base de datos
	module_db = None
	## Instancia del modulo audio
	module_audio = None


	##### Instancia de servicios
	tts = None
	stt = None
	nlu = None

	## Constructor
	def __init__(self, language, led_module, db_module, audio_module):
		############# Instancia de los modulos
		## Definimos el lenguaje de trabajo
		self.language = language
		## Instanciamos el módulo LED
		self.module_led = led_module
		## Instanciamos el módulo de base de datos
		self.module_db = db_module
		## Instanciamos el módulo de audio
		self.module_audio = audio_module

		############# Instancia del resto de servicios
		## Instanciamos el servicio TTS
		self.tts = TTSService(self)
		## Instanciamos el servicio STT
		self.stt = STTService(self)
		## Instanciamos el servicio NLU
		self.nlu = NLUService(self)

		############# Debug
		self.things["devices"]["ventilador"] = Switch("192.168.1.50", "FF:FF:FF:00:00:00", "ventilador")
		self.things["devices"]["bombilla"] = Bolb("192.168.1.51", "AF:AF:AF:00:00:00", "bombilla")
		self.things["ambiences"]["ambiente"] = Ambience("ambiente")

	## Método que despierta al servicio
	def wake(self):
		## Modificamos la valiza de estado
		self.wakeUp = True

		## Animamos los led con la animacion de despertar
		if self.module_led is not None:
			self.module_led.wakeup()

		## Mensaje de aviso
		print("Melissa is wake up")

	## Método que duerme al servicio
	def sleep(self):
		## Modificamos la valiza de estado
		self.wakeUp = False

		## Apagamos los led
		if self.module_led is not None:
			self.module_led.off()

		## Mensaje de aviso
		print("Melissa is sleeping")

	## Método que aborta el servicio
	def abort(self):
		## Modificamos la valiza de estado
		self.wakeUp = False

		## Apagamos los led
		if self.module_led is not None:
			self.module_led.off()

		## Mensaje de aviso
		print("See you soon!")
		
		## Salimos de la APP
		quit()

	## Método inicia el servicio de IoT
	def start_service(self):
		## Inicia el primer paso del servicio de IoT
		self.stt.start()

	## Método que recibe datos del servicio NLU
	def from_nlu(self, intent):
		## DEBUG - Mostramos Intent
		print(json.dumps(intent)) 