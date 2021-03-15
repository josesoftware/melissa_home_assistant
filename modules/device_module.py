#######################################################################
## Este módulo se encarga de la comunicacion con dispositivos de IoT ##
#######################################################################

## Importamos modulos necesarios
import requests
import ipaddress

## Clase que representa el módulo
class IoTDevice:

	## Atributos
	address = ipaddress.ip_address('255.255.255.255')

	## Constructor
	def __init__(self, address):
		## Fijamos la direccion IP
		self.address = ipaddress.ip_address(address)

	## Método que enviará al dispositivo la orden de encenderse
	def turn_on(self):

		## Enviamos una peticion GET
		return requests.get('http://%s/?relay=on' % self.address)

	## Método que enviara al dispositivo la orden de apagarse
	def turn_off(self):

		## Enviamos una peticion GET
		return requests.get('http://%s/?relay=off' % self.address)
