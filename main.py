# coding=utf-8

##################################
### Importaciones 		 #########
##################################
## Importamos diccionarios
from dictionaries.dictionary import LANGUAGE_DICTIONARY as LANGUAGES

## Importacion de objetos
from services.Melissa import MelissaService

#############################################
##	Instanciamos Módulos				   ##
#############################################
## Instanciamos el modulo controlador de los LED
LED_Module = None # Pixels()
## Instanciamos el modulo de base de datos
DB_Module = None # Pixels()
## Instanciamos el modulo controlador de audio
Audio_Module = None # Pixels()

##############################################
## Instanciamos servicios					##
##############################################
## Instanciamos el servicio Melissa
Melissa = MelissaService(LANGUAGES["EN-US"], LED_Module, DB_Module, Audio_Module)

## Iniciamos el servicio
Melissa.StartService()