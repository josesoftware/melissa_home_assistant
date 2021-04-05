###############################################################
## Componente que se dedica a llevar a cabo un intent        ##
###############################################################

## Importamos modulos
import json

## Importamos excepciones de objetos
from objects.Device import DeviceTargetMismatchException

class IntentProcessorService:
	## Instancia del servicio de IoT
	melissa = None

	## Constructor
	def __init__(self, melissaService):
		## Instanciamos el servicio Melissa
		self.melissa = melissaService

	## Método invocado desde el NLU
	def from_nlu(self, intents):
		## DEBUG
		json.dumps(intents, indent=4)

		## Recorre la lista de intents
		for intent in intents:
			## Siempre que el intent no venga vacío
			if intent:
				## Si el intent va dirigido a un dispositivo
				if 'device' in intent:
					## Controla excepciones
					try:
						## Recupera el intent de acción y lo lleva a cabo
						self.do_intent(self.melissa.things["devices"][intent['device']].do_intent(intent))

					except DeviceTargetMismatchException as e:
						## Escribe en el log el error
						self.melissa.stg.log_debug_write("Intent device mismatch target: '{target}', sended to: '{receiver}'".format(target=e.target, receiver=e.receiver), 'Device intent mismatch')

						## Pasa al siguiente ciclo
						continue

					except Exception as e:
						## Escribe en el log el error
						self.melissa.stg.log_debug_write("Unknown error processing device intent on device: '{target}', error: '{error}'".format(target=intent['device'], error=e), 'Device intent error')

						## Pasa al siguiente ciclo
						continue
				
				## Si el intent va dirigido a un ambiente
				elif 'ambience' in intent:
					## Lleva a cabo el intent
					self.do_intent(intent)

				## Si el intent es un comando
				elif 'command' in intent:
					## Lleva a cabo el intent
					self.do_intent(intent)
				
				## Si no se recogonoce el tipo de thing al que va dirigido el intent
				else:
					## Escribe en el log el error
					self.melissa.stg.log_debug_write("Unknown intent: '{intent}'".format(intent=intent), 'Not recognizer intent')

					## Pasa al siguiente ciclo
					continue

	## Método que lleva a cabo un intent de ejecución
	def do_intent(self, intentToDo):
		## DEBUG
		json.dumps(intentToDo, indent=4)
		print (intentToDo)

		## Duerme el servicio melissa una vez realiza todas las tareas
		self.melissa.sleep()
