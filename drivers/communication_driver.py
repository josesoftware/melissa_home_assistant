#######################################################################
## Este driver se encarga de las comunicacion                        ##
#######################################################################

## Importación de modulos
import json, requests, os

class CommunicationDriver:
	## Constructor
	def __init__(self):
		pass

	############## Métodos que tratan con dispositivos
	## Método que lleva a cabo un request de tipo GET
	def device_get_request(self, request):
		## Realizas el request
		return requests.get(request)

	## Método que hace un ping a un dispositivo
	def device_check_ping(self, addr):
		## Retornamos la baliza de estado
		return (os.system("ping -c 2 " + addr) == 0)