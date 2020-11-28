#######################################################################
## Objeto que representa un dispositivo de tipo Bolb (Bombilla) 	 ##
#######################################################################

## Importamos modulos necesarios
import requests
from ..libraries.lib_math import IntClamp as Clamp
from Device import IoTDevice as Parent

## Clase que representa el módulo
class Bolb(Parent):
	## Atributo color
	Color = '#000000'
	Intensity = 100

	## Constructor
	def __init__(self, address, mac, alias):
		# Constructor del objeto padre 
		Parent.__init__(self, address, mac, alias) 
  
	## Método que enviará al dispositivo la orden de encenderse
	def TurnON(self):
		## Enviamos una peticion GET
		return requests.get('http://%s/?light=on' % self.Address)

	## Método que enviara al dispositivo la orden de apagarse
	def TurnOFF(self):
		## Enviamos una peticion GET
		return requests.get('http://%s/?light=off' % self.Address)

	## Método que enviara al dispositivo la orden de cambiar a un color especifico
	def SetColor(self, color):
		## Fijamos el nuevo color
		self.Color = color

		## Enviamos una peticion GET
		return requests.get('http://{0}/?color={1}{2}'.format(self.Address, self.Color, format(int(self.Intensity * 255 / 100), 'x')))

	## Método que enviara al dispositivo la orden de cambiar a un color especifico
	def SetIntensity(self, intensity):
		## Fijamos la intensidad
		self.Intensity = Clamp(intensity, 0, 255)

		## Enviamos una peticion GET
		return requests.get('http://{0}/?color={1}{2}'.format(self.Address, self.Color, format(int(self.Intensity * 255 / 100), 'x')))
