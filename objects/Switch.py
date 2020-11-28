#######################################################################
## Objeto que representa un dispositivo de tipo Switch (Interruptor) ##
#######################################################################

## Importamos modulos necesarios
import requests
from Device import IoTDevice as Parent

## Clase que representa el módulo
class Switch(Parent):
	## Atributo de estado
	Status = 'off'

	## Constructor
	def __init__(self, address, mac, alias):
		# Constructor del objeto padre 
		Parent.__init__(self, address, mac, alias) 
  
	## Método que enviará al dispositivo la orden de encenderse
	def TurnON(self):
		## Modificamos el estado del rele
		self.Status = 'on'

		## Enviamos una peticion GET
		return requests.get('http://{0}/?relay={1}'.format(self.Address, self.Status))

	## Método que enviara al dispositivo la orden de apagarse
	def TurnOFF(self):
		## Modificamos el estado del rele
		self.Status = 'off'

		## Enviamos una peticion GET
		return requests.get('http://{0}/?relay={1}'.format(self.Address, self.Status))
