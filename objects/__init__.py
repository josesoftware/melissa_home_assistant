#######################################################################
## Cabecera del paquete de objetos					                 ##
#######################################################################

## Importamos módulos necesários
import json
from collections import namedtuple

## Clase que representa un Intent
class Intent:
    ## Método estático que crea un objeto 'Intent' desde un texto diccionario
    @staticmethod
    def GetObject(dictionary):
        return json.loads(json.dumps(dictionary), object_hook=Intent.FromJSON)

    ## Método estático que devuelve un 'namedTuple' de un texto JSON
    @staticmethod
    def FromJSON(jsonIntent):
        ## Retornaremos el 'namedTuple' obtenido del diccionario JSON
        return namedtuple('X', jsonIntent.keys())(*jsonIntent.values())