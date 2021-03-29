#######################################################################
## Objeto que representa un dispositivo de IoT						 ##
#######################################################################

## Importamos modulos necesarios
import ipaddress
from objects import Thing
from enum import Enum

## Enumerado que determina la categoria de un dispositivo
class DeviceCategory(Enum):
	Light = 0,
	Audio = 1,
	Temperature = 2,
	Abstract = 3


## Clase que representa el módulo
class IoTDevice(Thing):

	## Atributos comunes en todos los dispositivos
	address = ipaddress.ip_address('255.255.255.255')
	macAddress = 'FF:FF:FF:FF:FF'
	alias = 'Device'
	isAlive = False
	category = None

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
		## Se fija una categoria
		self.category = DeviceCategory.Abstract

	## Método que traduce un Intent en un request al dispositivo
	def do_intent(self, intent):
		pass