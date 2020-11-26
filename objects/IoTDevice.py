#######################################################################
## Este módulo se encarga de la comunicacion con dispositivos de IoT ##
#######################################################################

## Importamos modulos necesarios
import requests
import ipaddress

## Clase que representa el módulo
class IoTDevice:

	## Atributos
    IPAddress = ipaddress.ip_address('255.255.255.255')
    MACAddress = 'FF:FF:FF:FF:FF'
    Alias = 'Default'

	## Constructor
	def __init__(self, address):
		## Fijamos la direccion IP
		self.Address = ipaddress.ip_address(address)

	## Método que enviará al dispositivo la orden de encenderse
	def TurnON(self):

		## Enviamos una peticion GET
		return requests.get('http://%s/?relay=on' % self.Address)

	## Método que enviara al dispositivo la orden de apagarse
	def TurnOFF(self):

		## Enviamos una peticion GET
		return requests.get('http://%s/?relay=off' % self.Address)