#######################################################################
## Objeto que representa un dispositivo de IoT						 ##
#######################################################################

## Importamos modulos necesarios
import ipaddress, json
from enum import Enum

## Importa modulo del objeto padre
from objects import Thing

## Enumerado que determina la categoria de un dispositivo
class DeviceCategory(Enum):
	Light = 0,
	Audio = 1,
	Temperature = 2,
	Abstract = 3

#################################################
## Si el formato del JSON es erróneo
class BadJsonFormatException(Exception):
	## Constuctor de la excepción 
	def __init__(self, inJson, message="Bad JSON format for make Device Object"):
		self.inJson = inJson
		self.message = message
		super().__init__(self.message)

## Si la categoria no existe
class DeviceCategoryNotDefinedException(Exception):
	## Constuctor de la excepción 
	def __init__(self, category, message="Device category is not defined"):
		self.category = category
		self.message = message
		super().__init__(self.message)

## Si se desea procesar un intent que no es del dispositivo local
class DeviceTargetMismatchException(Exception):
	## Constuctor de la excepción 
	def __init__(self, target, receiver, message="Device target mismatch"):
		self.target = target
		self.receiver = receiver
		self.message = message
		super().__init__(self.message)

## Clase que representa el módulo
class IoTDevice(Thing):

	## Atributos comunes en todos los dispositivos
	address = ipaddress.ip_address('255.255.255.255')
	macAddress = 'FF:FF:FF:FF:FF'
	alias = 'Thing Device'
	isAlive = False
	category = None

	## Propiedades del dispositivo
	properties = { }

	## Constructor
	def __init__(self, address='255.255.255.255', mac='FF:FF:FF:FF:FF', alias='Thing Device', properties={}, category=DeviceCategory.Abstract):
		# Constructor del objeto padre 
		Thing.__init__(self)

		## Fijamos la direccion IP
		self.address = ipaddress.ip_address(address)
		## Fijamos la direccion MAC
		self.macAddress = mac
		## Fijamos el alias
		self.alias = alias
		## Se fija una categoria
		self.category = category

	@staticmethod
	## Método estático que devuelve un objeto de tipo device
	def from_json(json_string):
		## Controla excepciones
		try:
			## Recuepera los datos del objeto desde el JSON
			json_device = json.loads(json_string)

			## Definimos una categoria para el dispositivo
			_deviceCategory = None

			## Compara enumerados
			for name, member in DeviceCategory.__members__.items():
				## Si la categoria obtenida del JSON es encontrada
				if name == json_device["category"]:
					## Fija la categoria
					_deviceCategory = member
					## Sale del bucle
					break

			## Si no se ha recuperado una categoria, se retorna error
			if _deviceCategory is None:
				raise DeviceCategoryNotDefinedException(json_device["category"])

			## Construye la instancia de un dispositivo basandose en los datos del JSON
			device = IoTDevice(address=json_device["address"], mac=json_device["mac"], alias=json_device["alias"], properties=json_device["properties"].copy(), category=_deviceCategory)

			## Recorre la lista de intents
			for intent in json_device["intents"]:
				## Recorre el key, value de cada intent
				for key, value in intent.items():
					## Añade el intent a la lista
					device.intents[key] = value

			## Retorna el dispositivo
			return device

		except ValueError:
			## Devuelve error de conversión por un formato erroneo
			raise BadJsonFormatException(json_string)

	## Método que traduce un Intent de dispositivo en un Intent de ejecución que el sistema pueda llevar a cabo
	def do_intent(self, intent):
		## Define el intent de retorno
		returnIntent = {}

		## Si el intent no va dirigido a este objeto retornará error
		if intent['device'] != self.alias:
			raise DeviceTargetMismatchException(intent['device'], self.alias)

		## Recoge la plantilla del intent
		returnIntent = self.intents[intent['intent']]

		## Recorre los parámetros del intent para realizar la modificación
		for key, value in intent['parameters']:
			## Si existe una propiedad nombrada igual que el parametro
			if key in self.properties:
				## Modifica la propiedad
				self.properties[key] = value

			## Fija los parametros al intent de retorno
			returnIntent['parameters'][key] = value

		
		################## Parametros especiales
		## Direccion IP
		if 'ip-address' in returnIntent['parameters']:
			returnIntent['parameters']['ip-address'] = str(self.address)

		## Direccion Mac
		if 'mac-address' in returnIntent['parameters']:
			returnIntent['parameters']['mac-address'] = self.macAddress

		## Direccion Alias
		if 'alias' in returnIntent['parameters']:
			returnIntent['parameters']['alias'] = self.alias

		## Retorna el intent de ejecución
		return returnIntent