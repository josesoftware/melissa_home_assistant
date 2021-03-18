###############################################################
## Componente que se dedica a comprender un lenguaje natural ##
##-----------------------------------------------------------##
## Convierte textos de un lenguaje natural en intents        ##
###############################################################

## Importamos metodos de la libreria de utilidades
from libraries.lib_utils import count_words, multi_split

## Importamos diccionarios
from dictionaries import translations as TRANSLATIONS
from dictionaries.dictionary import COLOR_DICTIONARY as COLORS

### DEBUG
import json

## Definición del objeto
class NLUService:
	## Instancia del servicio de IoT
	melissa = None  

	## Constructor
	def __init__(self, melissaService):
		## Instanciamos el servicio Melissa
		self.melissa = melissaService   

	## Método que recibe datos del servicio STT
	def from_stt(self, sttInput):
		## DEBUG - Mostramos string
		print(sttInput)
		## DEBUG - Mostramos Intent
		print(json.dumps(self.match_commands(sttInput))) 

	## Método que recibe datos del servicio STT en busca de la WakeWord
	def match_wake_word(self, sttInput):
		## Recorremos cada uno de los wakeWords definidos
		for wakeWord in self.melissa.wakeWords:
			## Comprueba que el input del STT sea un WakeWord
			if sttInput == wakeWord:
				## Despierta el reconocimiento de voz
				self.melissa.wake()

				## Retorna True si el input del STT es un WakeWord
				return True

			## Por defecto retornará False para no despertar más servicios
			return False

	## Método que busca comandos en un input del servicio STT
	def match_commands(self, sttInput):
		## Separamos primero la hipotesis del STT mediante los separadores de comando
		commandPhrases = multi_split(sttInput, self.melissa.commandSplitters)

		## Definimos un Array de intents de retorno
		intentArray = [ ]

		## Recorremos la lista de frases obtenida tras aplicar separadores
		for phrase in commandPhrases:
			## Definimos una lista de posibles de ordenes
			possibleCommands = [ ]

			## Definimos el intent
			_intent = None

			####################################################################
			##### Nivel 1 de comprobación
			## Recorremos cada una de las ordenes internas de melissa
			for command in self.melissa.commands:
				## Si el comando está en la frase recibida del STT
				if command in phrase:
					## Marcamos la orden como posible
					possibleCommands.append(command)   

			

			## Si es una orden interna de melissa 
			if len(possibleCommands) != 0:
				####################################################################
				##### Nivel 2 de comprobación
				## Comprueba si existe más de una orden a procesar en la misma frase
				if len(possibleCommands) > 1:
					## Retorna Intent vacio
					return intentArray

				####################################################################
				##### Nivel 3 de comprobación
				## Comprobamos si es un comando simple 
				## Recorremos cada comando
				## Comprobamos si el comando tiene la misma cantidad de palabras que la frase
				if count_words(sttInput) == count_words(possibleCommands[0]):
					## Retornamos directamente el comando sin parametrizar
					return self.melissa.commands[possibleCommands[0]]
				else:
					## Componemos un intent basandonos en la plantilla
					_intent = self.melissa.commands[possibleCommands[0]]

				####################################################################
				##### Nivel 4 de comprobación
				### Determinamos el tipo de intent
				## Si el intent es de tipo exec
				if _intent["intent"] == "exec":
					continue
			## Si no es una orden interna de melissa
			else:
				####################################################################
				##### Nivel 5 de comprobación
				### Basándonos en el tipo de intent, identificamos los RAW commands
				## Ordenamos hacer match de dispositivo
				targetDevice = self.match_device(phrase)

				## Si se ha identificado el dispositivo
				if targetDevice is None:
					## Pasamos de ciclo
					continue

				## Añadimos el header del intent
				_intent = self.melissa.commands["device"]
					
				## Añadimos el dispositivo al intent
				_intent["device"] = targetDevice

				## Ordenamos hacer match de intent del dispositivo
				targetDeviceIntent = self.match_device_intent(targetDevice, phrase)

				## Si no se encuentra ningun intent
				if targetDeviceIntent is None:
					## Pasamos de ciclo
					continue

				## Añadimos el intent del dispositivo al intent general
				_intent["intent"] = targetDeviceIntent

				## Buscamos parametros "RAW" para llevar a cabo el intent
				_intent["parameters"] = self.match_intent_params(targetDevice, targetDeviceIntent, phrase)

				## Añadimos el intent al array de retorno
				intentArray.append(_intent)

		##### Exportación de resultados
		return intentArray

	## Método que busca parametros de un intent en una frase
	def match_intent_params(self, device, intent, phrase):
		## Definimos parametros de retorno
		ReturnParams = { }

		## Recorremos cada uno de los parametros del intet
		for parameter in self.melissa.devices[device].intents[intent]["parameters"]:
			## Si el parametro es "address" pasamos de cilco
			if parameter == "address":
				continue

			## Si el parametro es color
			if parameter == "color":
				## Recorremos la lista de colores
				for color in TRANSLATIONS.TRANSLATION_COLOR:
					## Si el color esta en la frase
					if color in phrase:
						ReturnParams["color"] = COLORS[TRANSLATIONS.TRANSLATION_COLOR[color]]["HEX"]

		## Retornamos resultados
		return ReturnParams

	## Método que busca un intent de dispositivo en una frase
	def match_device_intent(self, device, phrase):
		## Eliminamos Articulos y preposicones de la frase
		phrase = self.clear_string(phrase, True, True)

		## Recorremos la lista de dispositivos
		for intent in self.melissa.devices[device].intents:
			## Si se encuentra el intent dispositivo en la frase
			if TRANSLATIONS.TRANSLATION_DEVICE_COMMANDS[intent] in phrase:
				## Retornamos el intent a ejecutar
				return intent

		## Retornamos el objeto
		return None

	## Método que busca un dispositivo en la lista de dispositivos
	def match_device(self, phrase):
		## Recorremos la lista de dispositivos
		for device in self.melissa.devices:
			## Si se encuentra el dispositivo en la frase
			if device in phrase:
				## Retornamos el nombre del dispositivo
				return device

		## Retornamos el objeto
		return None

	## Método que limpia datos irrelevantes de un string
	def clear_string(self, str, clearArticles, clearPrepositions):
		# Si se desean limpiar los articulos
		if clearArticles:
			## Recorremos la lista de articulos
			for article in TRANSLATIONS.TRANSLATION_ARTICLES:
				str = str.replace(article, " ")

		# Si se desean limpiar las preposiciones
		if clearPrepositions:
			## Recorremos la lista de articulos
			for preposition in TRANSLATIONS.TRANSLATION_PREPOSITIONS:
				str = str.replace(preposition, " ")

		## Retornamos el string reparado
		return str