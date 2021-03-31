# coding=utf-8

##################################
### Importaciones 		 #########
##################################
## Importamos diccionarios
from dictionaries.dictionary import LANGUAGE_DICTIONARY as LANGUAGES
## Importamos driver de Hardware
from drivers import Hardware, RPIHat
## Importacion de objetos
from services.HAS import HomeAssistantService

#############################################
## Instancia del hardware                  ##
#############################################
hardware = Hardware.Make(RPIHat.Respeaker4Mic)

##############################################
## Instanciamos servicios					##
##############################################
## Instanciamos el servicio Melissa
melissa = HomeAssistantService(LANGUAGES["ES-ES"], hardware)

## Iniciamos el servicio
melissa.start_service()