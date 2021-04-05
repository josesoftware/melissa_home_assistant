#######################################################################
## Objeto que representa un dispositivo de tipo Bolb (Bombilla) 	 ##
#######################################################################

## Importamos modulos necesarios
import requests
from libraries.lib_math import int_clamp as Clamp
from objects.Device import IoTDevice as Parent
from objects import ThingCategory

## Clase que representa el módulo
class Bolb(Parent):
	## Atributo propios del objeto Bolb
	color = '#000000'
	intensity = 100
	status = 'off'

	## Constructor
	def __init__(self, address, mac, alias):
		## Constructor del objeto padre 
		Parent.__init__(self, address, mac, alias)

		## Fijamos una categoria de tipo Light (Luz)
		self.category = ThingCategory.Categories["Light"]

		## Inicializamos acciones disponibles
		self.init_intents()
  
	## Inicializamos Actions con variables reales
	def init_intents(self):
		## Acciones disponibles
		self.intents = {
			"turn on": { "request": "http://{address}/?light=on", "parameters": { "address": self.address } },
			"turn off": { "request": "http://{address}/?light=off", "parameters": { "address": self.address } },
			"color set": { "request": "http://{address}/?color={color}", "parameters": { "address": self.address, "color": self.color } },
			"intensity set": { "request": "http://{address}/?intensity={intensity}", "parameters": { "address": self.address, "intensity": self.intensity } },
			"modify": { "request": "http://{address}/?intensity={intensity}&color={color}", "parameters": { "address": self.address, "intensity": self.intensity, "color": self.color } }
		}

	## Método que traduce un Intent en un request al dispositivo
	def do_intent(self, intent, communicationModule):
		## Controlamos excepciones
		try:
			## Inicializamos el request basandonos en el 'intent'
			request = self.intents[intent["intent"]]

			#### MODIFICACIONES DE ESTADO
			## Si se pretender apagar el dispositivo
			if intent["intent"] == 'turn off':
				self.status = 'off'
			## Si se pretender encender el dispositivo
			if intent["intent"] == 'turn on':
				self.status = 'on'

			#### VALORES CRUDOS ( RAW )
			## Recorremos los parametros del request
			for parameter in intent["parameters"]:
				## Si hay un parametro color
				if parameter == 'color':
					## Modificamos el atributo color
					self.color = intent["parameters"][parameter]
					## Reescribimos el parametro
					request["parameters"][parameter] = intent["parameters"][parameter]

				## Si hay un parametro intensidad
				if parameter == 'intensity':
					## Modificamos el atributo color
					self.intensity = Clamp(int(intent["parameters"][parameter]), 0, 100)
					## Reescribimos el parametro
					request["parameters"][parameter] = Clamp(int(intent["parameters"][parameter]), 0, 100)

			## Enviamos una peticion GET
			return communicationModule.get_request(self, request["request"].format(**request["parameters"]))
		except:
			## Retornamos error
			return "Intent not defined for this device"