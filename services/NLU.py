###############################################################
## Componente que se dedica a comprender un lenguaje natural ##
##-----------------------------------------------------------##
## Convierte textos de un lenguaje natural en Intents        ##
###############################################################

## Importamos metodos de la libreria de utilidades
from libraries.lib_utils import CountWords, MultiSplit

## Importamos diccionarios
from dictionaries import translations as TRANSLATIONS
from dictionaries.dictionary import COLOR_DICTIONARY as COLORS

## Definición del objeto
class NLUService:
	## Instancia del servicio de IoT
	Melissa = None  

	## Constructor
	def __init__(self, melissaService):
		## Instanciamos el servicio Melissa
		self.Melissa = melissaService   

	## Método que recibe datos del servicio STT
	def FromSTT(self, sttInput):
		print(self.MatchCommands(sttInput)) 

	## Método que busca comandos en un input del servicio STT
	def MatchCommands(self, sttInput):
		## Separamos primero la hipotesis del STT mediante los separadores de comando
		commandPhrases = MultiSplit(sttInput, self.Melissa.CommandSplitters)

		## Definimos un Array de Intents de retorno
		IntentArray = [ ]

		## Recorremos la lista de frases obtenida tras aplicar separadores
		for phrase in commandPhrases:
			################# DEBUG
			## Mostramos el texto como debug
			print(phrase)
			################# END DEBUG

			## Definimos una lista de posibles de ordenes
			possibleCommands = [ ]

			## Definimos el intent
			_intent = None

			####################################################################
			##### Nivel 1 de comprobación
			## Recorremos cada una de las ordenes
			for command in self.Melissa.Commands:
				## Si el comando está en la frase recibida del STT
				if command in phrase:
					## Marcamos la orden como posible
					possibleCommands.append(command)   

			## Si no hay resultados pasamos de cilco
			if len(possibleCommands) == 0:
				## Pasamos de ciclo
				continue

			####################################################################
			##### Nivel 2 de comprobación
			## Comprueba si existe más de una orden a procesar en la misma frase
			if len(possibleCommands) > 1:
				## Retorna Intent vacio
				return IntentArray

			####################################################################
			##### Nivel 3 de comprobación
			## Comprobamos si es un comando simple 
			## Recorremos cada comando
			## Comprobamos si el comando tiene la misma cantidad de palabras que la frase
			if CountWords(sttInput) == CountWords(possibleCommands[0]):
				## Retornamos directamente el comando sin parametrizar
				return self.Melissa.Commands[possibleCommands[0]]
			else:
				## Componemos un intent basandonos en la plantilla
				_intent = self.Melissa.Commands[possibleCommands[0]]

			####################################################################
			##### Nivel 4 de comprobación
			### Determinamos el tipo de intent
			## Si el intent es de tipo exec
			if _intent["intent"] == "exec":
				####################################################################
				##### Nivel 5 de comprobación
				### Basándonos en el tipo de intent, identificamos los RAW commands
				## Ordenamos hacer match de dispositivo
				targetDevice = self.MatchDevice(phrase)

				## Si se ha identificado el dispositivo
				if targetDevice is None:
					## Pasamos de ciclo
					continue
					
				## Añadimos el dispositivo al intent
				_intent["parameters"]["device"] = targetDevice

				## Ordenamos hacer match de intent del dispositivo
				targetDeviceIntent = self.MatchDeviceIntent(targetDevice, phrase)

				## Si no se encuentra ningun intent
				if targetDeviceIntent is None:
					## Pasamos de ciclo
					continue

				## Añadimos el intent del dispositivo al intent general
				_intent["parameters"]["intent"] = targetDeviceIntent

				## Buscamos parametros "RAW" para llevar a cabo el intent
				self.MatchIntentParams(_intent["parameters"]["intent"], phrase)

			## Añadimos el intent al array de retorno
			IntentArray.append(_intent)



		##### Exportación de resultados
		return IntentArray

	## Método que busca parametros de un intent en una frase
	def MatchIntentParams(self, intent, phrase):
		## Recorremos cada uno de los parametros del intet
		for parameter in intent["parameters"]:
			## Si el parametro es "address" pasamos de cilco
			if parameter == "address":
				continue

			## Si el parametro es color
			if parameter == "color":
				## Recorremos la lista de colores
				for color in TRANSLATIONS.TRANSLATION_COLOR:
					## Si el color esta en la frase
					if color in phrase:
						intent["parameters"]["color"] = COLORS[TRANSLATIONS.TRANSLATION_COLOR[color]]["HEX"]

	## Método que busca un intent de dispositivo en una frase
	def MatchDeviceIntent(self, device, phrase):
		## Recorremos la lista de dispositivos
		for intent in self.Melissa.Devices[device].Intents:
			## Si se encuentra el intent dispositivo en la frase
			if TRANSLATIONS.TRANSLATION_DEVICE_COMMANDS[intent] in phrase:
				## Retornamos el intent a ejecutar
				return intent

		## Retornamos el objeto
		return None

	## Método que busca un dispositivo en la lista de dispositivos
	def MatchDevice(self, phrase):
		## Recorremos la lista de dispositivos
		for device in self.Melissa.Devices:
			## Si se encuentra el dispositivo en la frase
			if device in phrase:
				## Retornamos el nombre del dispositivo
				return device

		## Retornamos el objeto
		return None