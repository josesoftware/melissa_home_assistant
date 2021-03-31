#################################################################
## Objeto que representa el servicio de IoT 				   ##
#################################################################

## Importacion de modulos
import json

## Importamos servicios necesarios
from services.TTS import TTSService
from services.STT import STTService
from services.NLU import NLUService
from services.STG import StorageService

## Importamos dirvers
from drivers.database_driver import DatabaseDriver
from drivers.communication_driver import CommunicationDriver
from drivers.database_driver import DatabaseDriver
from drivers.audio_driver import AudioDriver
## Controlamos excepciones de importación de drivers conflictivos
try:
    from drivers.led_driver import Pixels
except:
    pass

## Importamos objetos
from objects.Switch import Switch
from objects.Bolb import Bolb
from objects.Ambience import Ambience


## Definición de la clase
class HomeAssistantService:
	#### Atributos estaticos
	## Idicador de estado
	wakeUp = False
	## Indicador de modo debug
	debugMode = False
	## Indicador de bloqueo
	locked = False
	## Lenguaje de trabajo del servicio
	language = None
	## Fija los datos referentes al hogar
	hive = {"id": "", "alias": "default"}

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
	## Instancia del hardware
	hardware = None
	## Instancia del driver de LED
	driver_led = None
	## Instancia del driver de base de datos
	driver_db = None
	## Instancia del driver de audio
	driver_audio = None
	## Instancia del driver de comunicacion
	driver_communication = None


	##### Instancia de servicios
	tts = None
	stt = None
	nlu = None
	stg = None
	ips = None

	## Constructor
	def __init__(self, language, hardware):
		#################################################
		## Definimos el lenguaje de trabajo
		self.language = language
		## Instanciamos el hardware
		self.hardware = hardware

		#################################################
		## Instanciamos el driver de base de datos
		self.driver_db = DatabaseDriver()
		## Instanciamos el driver de audio
		self.driver_audio = AudioDriver(self.hardware)
		## Instanciamos el driver de comunicaciones
		self.driver_communication = CommunicationDriver()
		## Instanciamos el driver de LED
		## Controlamos excepciones de inicializacion de drivers conflictivos
		try:
			self.driver_led = Pixels(ledCount=self.hardware.LED_COUNT)
		except:
			self.driver_led = None

		#################################################
		## Instanciamos el servicio TTS ( Text To Speech Service)
		self.tts = TTSService(self)
		## Instanciamos el servicio STT ( Speech To Text Service )
		self.stt = STTService(self)
		## Instanciamos el servicio NLU ( Natural Language Understanding Service )
		self.nlu = NLUService(self)
		## Instanciamos el servicio IPS ( Intent proccessor Service )
		self.ips = NLUService(self)
		## Instanciamos el servicio de almacenamiento
		self.stg = StorageService(self)

		#################################################
		## Recuperamos información dinámica de la máquina
		self.hardware.set_hardware_info(self.stg.get_machine_hostname(), self.stg.get_machine_id())

		#### TEST
		self.debugMode = True

		#################################################
		## Carga la configuración de la máquina
		self.stg.load_configfile()

		#################################################
		############# Debug
		self.things["devices"]["ventilador"] = Switch("192.168.1.50", "FF:FF:FF:00:00:00", "ventilador")
		self.things["devices"]["bombilla"] = Bolb("192.168.1.51", "AF:AF:AF:00:00:00", "bombilla")
		self.things["ambiences"]["relax"] = Ambience("relax")
		self.things["commands"]["reproduce música"] = "test"

	## Método que despierta al servicio
	def wake(self):
		## Si el servicio ya estaba despierto
		if self.wakeUp:
			## Invoca al modo escuchar
			self.listening()

			## Sale del método
			return

		## Modificamos la valiza de estado
		self.wakeUp = True

		## Animamos los led con la animacion de despertar
		if self.driver_led is not None:
			self.driver_led.wakeup()

		## Mensaje de aviso
		print("Melissa is wake up")

	## Método que aplica el modo scuchar al servicio melissa
	def listening(self):
		## Animamos los led con la animacion de despertar
		if self.driver_led is not None:
			self.driver_led.listen()

		## Mensaje de aviso
		print("Listening commands...")

	## Método que aplica el modo pensar al servicio melissa
	def thinking(self):
		## Animamos los led con la animacion de despertar
		if self.driver_led is not None:
			self.driver_led.think()

		## Mensaje de aviso
		print("Finding intents...")

	## Método que duerme al servicio
	def sleep(self):
		## Modificamos la valiza de estado
		self.wakeUp = False

		## Apagamos los led
		if self.driver_led is not None:
			self.driver_led.off()

		## Mensaje de aviso
		print("Melissa is sleeping")

	## Método que aborta el servicio
	def abort(self):
		## Modificamos la valiza de estado
		self.wakeUp = False

		## Apagamos los led
		if self.driver_led is not None:
			self.driver_led.off()

		## Mensaje de aviso
		print("See you soon!")
		
		## Salimos de la APP
		quit()

	## Método inicia el servicio de IoT
	def start_service(self):
		## Inicia el primer paso del servicio de IoT
		self.stt.start()

	## Método que recibe datos del servicio NLU
	def from_nlu(self, intents):
		## Recurre cada uno de los intents
		#for intent in intents:
			## Cuando el intent es un comando
		#	if 'command' in intent.keys():
				##### DEBUG
				## Si el intent es el comando "pon musica"
		#		if intent["command"] == "pon musica":
		#			import os

		#			file = "/var/www/html/python/audio/audio8.mp3"
		#			os.system("mpg123 " + file)

					## Fijamos el color a los led
		#			self.driver_led.think()
		#	else:
		## DEBUG - Mostramos Intent
		print(json.dumps(intents, indent=4))
			## Si hay un dispositivo en el intent
			## if "device" in intent.keys():
				## Recupera el dispositivo
				## device = self.things["devices"][intent["device"]]
				## Ejecuta el intent en el propio dispositivo
				## print ("Intent result: " + str(device.do_intent(intent, self.driver_communication)))
				## Sale del método
				## return

		## Duerme el servicio cuando termina
		self.sleep()

	## Método que configura al servicio Melissa como confundida
	def has_confusion(self, question=None):
		## Si no se ha definido una pregunta
		if question is None:
			## Mensaje debug
			question = "Service confused. Try again and with more specific command."

		## Mensaje debug
		print (question)