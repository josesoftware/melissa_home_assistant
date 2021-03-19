# coding=utf-8

##################################
### Importaciones 		 #########
##################################
## Importamos diccionarios
from dictionaries.dictionary import LANGUAGE_DICTIONARY as LANGUAGES
from modules.database_module import DatabaseModule
from modules.communication_module import CommunicationModule
## Controlamos excepciones de importación de modulos conflictivos
try:
    from modules.led_module import Pixels
except:
    pass
## Importacion de objetos
from services.Melissa import MelissaService

#############################################
##	Instanciamos Módulos				   ##
#############################################
## Instanciamos el modulo controlador de los LED
## Controlamos excepciones de inicializacion de modulos conflictivos
try:
    ledModule = Pixels()
except:
    ledModule = None
## Instanciamos el modulo de base de datos
dbModule = DatabaseModule # Pixels()
## Instanciamos el modulo controlador de audio
audioModule = None # Pixels()
## Instanciamos el modulo de comunicación
communicationModule = CommunicationModule()

##############################################
## Instanciamos servicios					##
##############################################
## Instanciamos el servicio Melissa
melissa = MelissaService(LANGUAGES["ES-ES"], ledModule, dbModule, audioModule, communicationModule)

## Iniciamos el servicio
melissa.start_service()
print(dbModule)