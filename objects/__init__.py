#######################################################################
## Cabecera del paquete de objetos					                 ##
#######################################################################

## Importamos módulos necesários
import json
from collections import namedtuple
from string import Formatter

## Clase que representa un Intent
class Intent:
	## Método estático que crea un objeto 'Intent' desde un texto diccionario
	@staticmethod
	def get_object(dictionary):
		return json.loads(json.dumps(dictionary), object_hook=Intent.from_json)

	## Método estático que devuelve un 'namedTuple' de un texto JSON
	@staticmethod
	def from_json(jsonIntent):
		## Retornaremos el 'namedTuple' obtenido del diccionario JSON
		return namedtuple('X', jsonIntent.keys())(*jsonIntent.values())

	## Método que extrae parametros de un string formateado
	@staticmethod
	def get_format_string_parameters(inString):
		## Retornamos array de parametros
		return [fname for _, fname, _, _ in Formatter().parse(inString) if fname]