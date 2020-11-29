#######################################################################
## Objeto que representa un dispositivo de tipo Bolb (Bombilla) 	 ##
#######################################################################

## Importamos modulos necesarios
import requests
from libraries.lib_math import IntClamp as Clamp
from Device import IoTDevice as Parent

## Clase que representa el módulo
class Bolb(Parent):
	## Atributo color
	Color = '#000000'
	Intensity = 100

	## Definimos acciones disponibles
	Actions = { }

	## Constructor
	def __init__(self, address, mac, alias):
		## Constructor del objeto padre 
		Parent.__init__(self, address, mac, alias)

		## Inicializamos acciones disponibles
		self.InitActions()
  
	## Inicializamos Actions con variables reales
	def InitActions(self):
		## Acciones disponibles
		self.Actions = {
			"turn on": { "url": "http://{address}/?light=on", "params": { "address": self.Address } },
			"turn off": { "url": "http://{address}/?light=off", "params": { "address": self.Address } },
			"color set": { "url": "http://{address}/?color={color}", "params": { "address": self.Address, "color": self.Color } },
			"intensity set": { "url": "http://{address}/?intensity={intensity}", "params": { "address": self.Address, "intensity": self.Intensity } }
		}

	## Método que traduce un Intent en un request al dispositivo
	def DoIntent(self, intent):
		## Inicializamos el request basandonos en el action
		IntentRequest = self.Actions[intent.Action]

		## Recorremos los parametros del request
		for parameter in intent.Parameters:
			## Reescribimos el parametro
			IntentRequest["params"][parameter.Key] = parameter.Value

		## Enviamos una peticion GET
		return self.GET_Request(IntentRequest["url"].format(**IntentRequest["params"]))