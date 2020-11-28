#######################################################################
## Objeto que representa un dispositivo de tipo Switch (Interruptor) ##
#######################################################################

## Importamos modulos necesarios
import requests
from Device import IoTDevice as Parent

## Clase que representa el módulo
class Switch(Parent):
	## Constructor
	def __init__(self, address, mac, alias):
		# Constructor del objeto padre 
		Parent.__init__(self, address, mac, alias) 
  
	## Método que enviará al dispositivo la orden de encenderse
	def TurnON(self):
		## Enviamos una peticion GET
		return requests.get('http://%s/?relay=on' % self.Address)

	## Método que enviara al dispositivo la orden de apagarse
	def TurnOFF(self):
		## Enviamos una peticion GET
		return requests.get('http://%s/?relay=off' % self.Address)
