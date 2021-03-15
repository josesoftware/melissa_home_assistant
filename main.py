# coding=utf-8

##################################
### Importaciones 		 #########
##################################
## Importamos diccionarios
from dictionaries.dictionary import LANGUAGE_DICTIONARY as LANGUAGES
from modules.database_module import DatabaseModule
## Importacion de objetos
from services.Melissa import MelissaService

#############################################
##	Instanciamos Módulos				   ##
#############################################
## Instanciamos el modulo controlador de los LED
ledModule = None # Pixels()
## Instanciamos el modulo de base de datos
dbModule = DatabaseModule # Pixels()
## Instanciamos el modulo controlador de audio
audioModule = None # Pixels()

##############################################
## Instanciamos servicios					##
##############################################
## Instanciamos el servicio Melissa
melissa = MelissaService(LANGUAGES["ES-ES"], ledModule, dbModule, audioModule)

## Iniciamos el servicio
melissa.start_service()
print(dbModule)