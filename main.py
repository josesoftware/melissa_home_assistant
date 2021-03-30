# coding=utf-8

##################################
### Importaciones 		 #########
##################################
## Importamos diccionarios
from dictionaries.dictionary import LANGUAGE_DICTIONARY as LANGUAGES
## Importamos driver de Hardware
from drivers import Hardware, RPIHat
## Importacion de objetos
from services.Melissa import MelissaService

#############################################
## Instancia del hardware                  ##
#############################################
hardware = Hardware(1, 2, 0)## Hardware.Make(RPIHat.Respeaker4Mic)

##############################################
## Instanciamos servicios					##
##############################################
## Instanciamos el servicio Melissa
melissa = MelissaService(LANGUAGES["ES-ES"], hardware)

## Iniciamos el servicio
melissa.start_service()