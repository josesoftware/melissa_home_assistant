#######################################################################
## Este módulo se encarga de las comunicacion                        ##
#######################################################################

## Importación de modulos
import json, requests, os

class CommunicationModule:
	## Constructor
	def __init__(self):
		pass

	############## Métodos que tratan con dispositivos
	## Método que lleva a cabo un request de tipo GET
	def device_get_request(self, device, intent):
		## Primero comprueba que hay conectividad con el dispositivo
		if self.device_check_ping(device):
			## Inicializamos el request basandonos en el 'intent'
			request = device.intents[intent]
			## Realizas el request
			return requests.get(request["request"].format(**request["parameters"]))

		## Retorna nulo si no se ha podido llevar a cabo
		return None

	## Método que hace un ping a un dispositivo
	def device_check_ping(self, device):
		## Determinamos si el dispositivo esta acccesible
		device.isAlive = (os.system("ping -c 2 " + str(device.address)) == 0)
		## Retornamos la baliza de estado
		return device.isAlive