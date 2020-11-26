#######################################################################
## Objeto que representa un dispositivo de IoT						 ##
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
	def __init__(self, address, mac, alias):
		## Fijamos la direccion IP
		self.Address = ipaddress.ip_address(address)
		## Fijamos la direccion MAC
		self.MACAddress = mac
		## Fijamos el alias
		self.Alias = alias