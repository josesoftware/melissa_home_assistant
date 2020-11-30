#######################################################################
## Objeto que representa un dispositivo de tipo Switch (Interruptor) ##
#######################################################################

## Importamos modulos necesarios
import requests
from objects.Device import IoTDevice as Parent

## Clase que representa el módulo
class Switch(Parent):
	## Atributo de estado
	Status = 'off'

	## Constructor
	def __init__(self, address, mac, alias):
		# Constructor del objeto padre 
		Parent.__init__(self, address, mac, alias)

		## Inicializamos acciones disponibles
		self.InitIntents()
  
	## Inicializamos Actions con variables reales
	def InitIntents(self):
		## Acciones disponibles
		self.Intents = {
			"turn on": { "request": "http://{address}/?relay=on", "parameters": { "address": self.Address } },
			"turn off": { "request": "http://{address}/?relay=off", "parameters": { "address": self.Address } }
		}
  
	## Método que traduce un Intent en un request al dispositivo
	def DoIntent(self, intent):
		## Controlamos excepciones
		try:
			## Inicializamos el request basandonos en el 'intent'
			request = self.Intents[intent["intent"]]


			#### MODIFICACIONES DE ESTADO
			## Si se pretender apagar el dispositivo
			if intent["intent"] == 'turn off':
				self.Status = 'off'
			## Si se pretender encender el dispositivo
			if intent["intent"] == 'turn on':
				self.Status = 'on'


			## Enviamos una peticion GET
			return self.GET_Request(request["request"].format(**request["parameters"]))
		except:
			## Retornamos error
			return "Intent not defined for this device"
