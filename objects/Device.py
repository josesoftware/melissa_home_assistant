#######################################################################
## Objeto que representa un dispositivo de IoT						 ##
#######################################################################

## Importamos modulos necesarios
import ipaddress
import requests
from objects import Thing

## Clase que representa el módulo
class IoTDevice(Thing):

	## Atributos comunes en todos los dispositivos
	address = ipaddress.ip_address('255.255.255.255')
	macAddress = 'FF:FF:FF:FF:FF'
	alias = 'Device'
	isAlive = False

	## Constructor
	def __init__(self, address, mac, alias):
		# Constructor del objeto padre 
		Thing.__init__(self)

		## Fijamos la direccion IP
		self.address = ipaddress.ip_address(address)
		## Fijamos la direccion MAC
		self.macAddress = mac
		## Fijamos el alias
		self.alias = alias

	## Método que ejecuta un request mediante GET
	def get_request(self, request):
		return requests.get(request)

	## Método que traduce un Intent en un request al dispositivo
	def do_intent(self, intent):
		pass