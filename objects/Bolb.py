#######################################################################
## Objeto que representa un dispositivo de tipo Bolb (Bombilla) 	 ##
#######################################################################

## Importamos modulos necesarios
import requests
from libraries.lib_math import IntClamp as Clamp
from objects.Device import IoTDevice as Parent

## Clase que representa el módulo
class Bolb(Parent):
	## Atributo propios del objeto Bolb
	Color = '#000000'
	Intensity = 100
	Status = 'off'

	## Constructor
	def __init__(self, address, mac, alias):
		## Constructor del objeto padre 
		Parent.__init__(self, address, mac, alias)

		## Inicializamos acciones disponibles
		self.InitIntents()
  
	## Inicializamos Actions con variables reales
	def InitIntents(self):
		## Acciones disponibles
		self.Intents = {
			"turn on": { "request": "http://{address}/?light=on", "parameters": { "address": self.Address } },
			"turn off": { "request": "http://{address}/?light=off", "parameters": { "address": self.Address } },
			"color set": { "request": "http://{address}/?color={color}", "parameters": { "address": self.Address, "color": self.Color } },
			"intensity set": { "request": "http://{address}/?intensity={intensity}", "parameters": { "address": self.Address, "intensity": self.Intensity } }
		}

	## Método que traduce un Intent en un request al dispositivo
	def DoIntent(self, intent):
		## Controlamos excepciones
		try:
			## Inicializamos el request basandonos en el 'intent'
			request = self.Intents[intent["intent"]]


			#### MODIFICACIONES DE ESTADO
			## Si se pretender apagar el dispositivo
			if intent["action"] == 'turn off':
				self.Status = 'off'
			## Si se pretender encender el dispositivo
			if intent["action"] == 'turn on':
				self.Status = 'on'


			#### VALORES CRUDOS ( RAW )
			## Recorremos los parametros del request
			for parameter in intent["parameters"]:
				## Si hay un parametro color
				if parameter == 'color':
					## Modificamos el atributo color
					self.Color = intent["parameters"][parameter]
					## Reescribimos el parametro
					request["parameters"][parameter] = intent["parameters"][parameter]

				## Si hay un parametro intensidad
				if parameter == 'intensity':
					## Modificamos el atributo color
					self.Intensity = Clamp(int(intent["parameters"][parameter]), 0, 100)
					## Reescribimos el parametro
					request["parameters"][parameter] = Clamp(int(intent["parameters"][parameter]), 0, 100)

			## Enviamos una peticion GET
			return self.GET_Request(request["request"].format(**request["parameters"]))
		except:
			## Retornamos error
			return "Intent not defined for this device"