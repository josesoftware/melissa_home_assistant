#######################################################################
## Objeto que representa un dispositivo de tipo Switch (Interruptor) ##
#######################################################################

## Importamos modulos necesarios
import requests
from objects.Device import IoTDevice as Parent

## Clase que representa el módulo
class Switch(Parent):
	## Atributo de estado
	status = 'off'

	## Constructor
	def __init__(self, address, mac, alias):
		# Constructor del objeto padre 
		Parent.__init__(self, address, mac, alias)

		## Inicializamos acciones disponibles
		self.init_intents()
  
	## Inicializamos Actions con variables reales
	def init_intents(self):
		## Acciones disponibles
		self.intents = {
			"turn on": { "request": "http://{address}/?relay=on", "parameters": { "address": self.address } },
			"turn off": { "request": "http://{address}/?relay=off", "parameters": { "address": self.address } }
		}
  
	## Método que traduce un Intent en un request al dispositivo
	def do_intent(self, intent):
		pass
