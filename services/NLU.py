###############################################################
## Componente que se dedica a comprender un lenguaje natural ##
##-----------------------------------------------------------##
## Convierte textos de un lenguaje natural en intents        ##
###############################################################

## Importamos metodos de la libreria de utilidades
from libraries.lib_utils import count_words, multi_split, merge_array, int_clamp

## Importamos diccionarios
from dictionaries import translations as TRANSLATIONS
from dictionaries.dictionary import COLOR_DICTIONARY as COLORS

## Importamos modulos
import json, re

## Definición del objeto
class NLUService:
	## Instancia del servicio de IoT
	melissa = None  

	## Lista de ordnenes
	THING_INTENT_PATTERN = { 
		"command": { "command": "", "parameters": { } },
		"ambience": { "ambience": "", "intent": "", "parameters": { } },
		"device": { "device": "", "intent": "", "parameters": { } }
	}
	## Lista de separadores de ordnenes
	COMMAND_SPLITTER = [
		"y después",
		"y luego"
	] 

	## Constructor
	def __init__(self, melissaService):
		## Instanciamos el servicio Melissa
		self.melissa = melissaService   

	## Método que recibe datos del servicio STT
	def from_stt(self, sttInput):
		## Pone al servicio melissa en modo pensar
		# self.melissa.thinking()

		## Retorna la lista de intents detectada
		self.melissa.ips.from_nlu(self.match_intents(sttInput))

	## Método que determina con que tipo de thing se desea tratar
	def match_thing(self, intentPhrase):
		###########################################
		#### Busca dispositivos en primer lugar
		## Si se ha identificado un dispositivo
		if self.match_device(intentPhrase) is not None:
			## Retornará device para salir del metodo
			return "device"

		###########################################
		#### Busca dispositivos en segundo lugar
		## Si se ha identificado el dispositivo
		if self.match_ambience(intentPhrase) is not None:
			## Retornará device para salir del metodo
			return "ambience"

		###########################################
		#### Busca comandos en tercer lugar
		## Recorremos cada una de las ordenes internas de melissa
		for command in self.melissa.things["commands"]:
			## Si el comando está en la frase recibida del STT
			if command in intentPhrase:
				## Retornará command para salir del metodo
				return "command"
		
		## Por defecto retornará None para indicar que no se debe hacer nada
		return None

	## Método que busca comandos en un input del servicio STT
	def match_intents(self, sttInputs):
		## Combinamos las frases provenientes del STT ( Habilita compatiblidad de multichannel de audio )
		sttInputs = merge_array(sttInputs)

		## Definimos un Array de intents de retorno
		intentArray = [ ]

		## Recorremos cada canal de audio
		for sttInput in sttInputs:
			## Separamos primero la hipotesis del STT mediante los separadores de comando
			commandPhrases = multi_split(sttInput, self.COMMAND_SPLITTER)

			## Definimos un Array de intents por canal
			intentChannel = [ ]

			## Recorremos la frase en cada uno de los canales de audio
			for phrase in commandPhrases:
				## Elimina espacios innecesarios
				phrase = phrase.strip()

				## Definimos una lista de posibles de ordenes
				possibleCommands = []

				## Definimos el intent
				_intent = None

				####################################################################
				##### Nivel 1 de comprobación -> Determinar con que tipo de thing se intenta tratar
				_thing = self.match_thing(phrase)

				## Si el thing retornado es None, pasamos al siguiente ciclo
				if _thing is None:
					continue

				## Si el tipo de thing es un comando
				if _thing == "command":
					############################################################
					## Nivel 2 de comprobación de comandos					  ##
					############################################################
					## Recorremos cada una de las ordenes internas de melissa
					for command in self.melissa.things["commands"]:
						## Si el comando está en la frase recibida del STT
						if command in phrase:
							## Si el comando no esta ya en la lista
							if command not in possibleCommands:
								## Marcamos la orden como posible
								possibleCommands.append(command) 

				

					## Si es una orden interna de melissa 
					if len(possibleCommands) != 0:
						## Comprueba si existe más de una orden a procesar en la misma frase
						if len(possibleCommands) > 1:
							## Retorna Intent vacio
							return intentArray

						####################################################################
						##### Nivel 3 de comprobación
						## Comprobamos si es un comando simple 
						## Recorremos cada comando
						## Comprobamos si el comando tiene la misma cantidad de palabras que la frase
						if count_words(phrase) == count_words(possibleCommands[0]):
							## Componemos un intent basandonos en la plantilla
							_intent = self.THING_INTENT_PATTERN["command"]

							## Fijamos el comando
							_intent["command"] = possibleCommands[0]
						else:
							continue

						####################################################################
						##### Nivel 4 de comprobación
						### Determinamos el tipo de intent
						## Si el intent es de tipo exec
						if _intent["command"] == "exec":
							continue

				## Si el intent quiere tratar con dispositivos
				elif _thing == "device":
					### Basándonos en el tipo de intent, identificamos los RAW commands
					## Ordenamos hacer match de dispositivo
					targetDevice = self.match_device(phrase)

					## Añadimos el header del intent
					_intent = self.THING_INTENT_PATTERN["device"]
						
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
					_intent["parameters"] = self.match_intent_params("devices", targetDevice, targetDeviceIntent, phrase)

				## Si el intent quiere tratar con ambientes
				elif _thing == "ambience":
					### Basándonos en el tipo de intent, identificamos los RAW commands
					## Ordenamos hacer match de dispositivo
					targetAmbience = self.match_ambience(phrase)

					## Añadimos el header del intent
					_intent = self.THING_INTENT_PATTERN["ambience"]
						
					## Añadimos el ambiente al intent
					_intent["ambience"] = targetAmbience

					## Ordenamos hacer match de intent del dispositivo
					targetAmbienceIntent = self.match_ambience_intent(targetAmbience, phrase)

					## Si no se encuentra ningun intent
					if targetAmbienceIntent is None:
						## Pasamos de ciclo
						continue

					## Añadimos el intent del dispositivo al intent general
					_intent["intent"] = targetAmbienceIntent

					## Buscamos parametros "RAW" para llevar a cabo el intent
					_intent["parameters"] = self.match_intent_params("ambiences", targetAmbience, targetAmbienceIntent, phrase)

				## Añadimos el intent al array de retorno si no es Nulo
				if _intent is not None:
					intentChannel.append(_intent.copy())

			## Añadimos el intent channel al intent array de retorno
			intentArray.append(intentChannel.copy())

		## Combina el array de intents y lo exporta
		return self.merge_intents(intentArray)

	## Método que combina un array de intents
	def merge_intents(self, intentArray):
		## Si el array viene vacio retornará vacío
		if not intentArray:
			return []

		## Declara el array de retorno
		returnArray = []

		## Recupera primero la cantidad de intents por canal
		for intentChannel in intentArray:
			## Si el array de intents del canal de audio actual no viene vacio
			if intentChannel:
				## Si aun no se han añadido intents a la lista se hace
				if not returnArray:
					## Añadimos los intents del primer canal
					returnArray = intentChannel.copy()

				## Si ya se habian añadido
				else:
					#### Comprobamos el recuento de intents del array de retorno en comparacion con los intents del canal de audio actual
					## Si tienen la misma longitud
					if len(returnArray) == len(intentChannel):
						## Recorreremos la lista 
						for i in range(len(returnArray)):
							## Comprueba que la lista de retorno y la lista del canal de audio actual tengan la misma estructura
							if set(returnArray[i].keys()) == set(intentChannel[i].keys()):
								## Si el intent procesa un comando
								if "command" in returnArray[i].keys():

									## Si el comando no es igual
									if returnArray[i]['command'] != intentChannel[i]['command']:

										## Retorna array vacío
										return [{ "question": "match_confusion_general", "parameters": { } }]

								## Si el intent procesa un dispositivo
								elif "device" in returnArray[i].keys():
									## Si el dispositivo no es igual
									if returnArray[i]['device'] != intentChannel[i]['device']:

										## Retorna intent de confusion
										return [{ "question": "match_confusion_device", "parameters": { "devices": [returnArray[i]['device'], intentChannel[i]['device']] } }]
									
									## Si el dispositivo es el mismo
									else:
										## Si el intent no es el mismo
										if returnArray[i]['intent'] != intentChannel[i]['intent']:

											## Retorna intent de confusion
											return [{ "question": "match_confusion_device_intent", "parameters": { "device": returnArray[i]['device'], "intents": [returnArray[i]['intent'], intentChannel[i]['intent']] } }]

										## Si el intent es el mismo
										else:
											## Si el intent de retorno no tiene parametros
											if not returnArray[i]['parameters']:

												## Añade los parametros del intent devuelto por el canal de audio actual
												returnArray[i]['parameters'] = intentChannel[i]['parameters']
											
											## Si el intent ya tenia parametros
											else:
												## Recorre los parametros del intent del canal de audio actual
												for parameter in intentChannel[i]['parameters']:

													## Comprueba si el parametro existe en el intent de retorno
													if parameter in returnArray[i]['parameters']:

														## Compara el valor del parametro del intent de retorno con el del canal de audio actual
														if returnArray[i]['parameters'][parameter] != intentChannel[i]['parameters'][parameter]:

															#################### COLOR
															##########################
															if parameter == 'color':
																## Retorna error de confusión por color
																return [{ "question": "match_confusion_intent_parameter_color", "parameters": { "colors": [returnArray[i]['parameters'][parameter], parameter] } }]

													## Si el parametro no está en la lista
													else:

														## Se añade el parametro a la lista de retorno
														returnArray[i]['parameters'][parameter] = parameter
								
								## Si el intent procesa un ambiente
								elif "ambience" in returnArray[i].keys():
									## Si el ambiente no es igual
									if returnArray[i]['ambience'] != intentChannel[i]['ambience']:
										## Retorna intent de confusion
										return [{ "question": "match_confusion_ambience", "parameters": { "ambiences": [returnArray[i]['ambience'], intentChannel[i]['ambience']] } }]
									
									## Si el dispositivo es el mismo
									else:
										## Si el intent no es el mismo
										if returnArray[i]['intent'] != intentChannel[i]['intent']:
											## Retorna intent de confusion
											return [{ "question": "match_confusion_ambience_intent", "parameters": { "ambienec": returnArray[i]['ambienec'], "intents": [returnArray[i]['intent'], intentChannel[i]['intent']] } }]

										## Si el intent es el mismo
										else:
											## Si el intent de retorno no tiene parametros
											if not returnArray[i]['parameters']:

												## Añade los parametros del intent devuelto por el canal de audio actual
												returnArray[i]['parameters'] = intentChannel[i]['parameters']
											
											## Si el intent ya tenia parametros
											else:
												## Recorre los parametros del intent del canal de audio actual
												for parameter in intentChannel[i]['parameters']:

													## Comprueba si el parametro existe en el intent de retorno
													if parameter in returnArray[i]['parameters']:

														## Compara el valor del parametro del intent de retorno con el del canal de audio actual
														if returnArray[i]['parameters'][parameter] != intentChannel[i]['parameters'][parameter]:

															#################### COLOR
															##########################
															if parameter == 'color':
																## Retorna error de confusión por color
																return [{ "question": "match_confusion_intent_parameter_color", "parameters": { "colors": [returnArray[i]['parameters'][parameter], parameter] } }]

													## Si el parametro no está en la lista
													else:
														## Se añade el parametro a la lista de retorno
														returnArray[i]['parameters'][parameter] = parameter

							## Si la estructura es distinta
							else:
								## Indicamos que el servicio está confundido
								return [{ "question": "match_confusion_intent", "parameters": { } }]
					
					## Si el array de retorno es mas largo
					else:
						## Indicamos que el servicio está confundido
						return [{ "question": "match_confusion_general", "parameters": { } }]


		## Retorna array vacío
		return returnArray

	###### Metodos que buscan atributos RAW
	## Método que busca parametros de un intent en una frase
	def match_intent_params(self, category, thing, intent, phrase):
		## Definimos parametros de retorno
		returnParams = { }

		## Recupera la lista de enteros en la frase
		integersInPhrase = re.findall(r'\d+', phrase)

		## Recorremos cada uno de los parametros del intet
		for parameter in self.melissa.things[category][thing].intents[intent]["parameters"]:
			## Si el parametro es color
			if parameter == "color":
				## Recorremos la lista de colores
				for color in TRANSLATIONS.TRANSLATION_COLOR:
					## Si el color esta en la frase
					if color in phrase:
						returnParams["color"] = COLORS[TRANSLATIONS.TRANSLATION_COLOR[color]]["HEX"]

			## Si el parametro es intensidad
			if parameter == "intensity":
				## Si la lista de enteros es igual a 1
				if len(integersInPhrase) == 1:
					## Fijamose la intensidad
					returnParams["intensity"] = int_clamp(integersInPhrase[0], (self.melissa.things[category][thing].properties['intensity']['min'] if 'min' in self.melissa.things[category][thing].properties['intensity'] else 0), (self.melissa.things[category][thing].properties['intensity']['max'] if 'max' in self.melissa.things[category][thing].properties['intensity'] else 100))
				else:
					## Fijamose la intensidad
					for key, value in TRANSLATIONS.TRANSLATION_NUMBER.items():
						## Si el color esta en la frase
						if key in phrase:
							## Fijamose el volumen
							returnParams["volume"] = value * 10

			## Si el parametro es volumen
			if parameter == "volume":
				## Si la lista de enteros es igual a 1
				if len(integersInPhrase) == 1:
					## Fijamose el volumen
					returnParams["volume"] = int_clamp(integersInPhrase[0], (self.melissa.things[category][thing].properties['volume']['min'] if 'min' in self.melissa.things[category][thing].properties['volume'] else 0), (self.melissa.things[category][thing].properties['volume']['max'] if 'max' in self.melissa.things[category][thing].properties['volume'] else 100))
				else:
					## Recorremos la lista de colores
					for key, value in TRANSLATIONS.TRANSLATION_NUMBER.items():
						## Si el color esta en la frase
						if key in phrase:
							## Fijamose el volumen
							returnParams["volume"] = value * 10

		## Retornamos resultados
		return returnParams

	###### Métodos que operan con Ambientes ( Ambiences )
	## Método que busca un intent de ambiente en una frase
	def match_ambience_intent(self, ambience, phrase):
		## Eliminamos Articulos y preposicones de la frase
		phrase = self.clear_string(phrase, True, True)

		## Recorremos la lista de ambientes
		for intent in self.melissa.things["ambiences"][ambience].intents:
			## Recorre cada uno de los sinonimos de traduccion
			for synonymous in TRANSLATIONS.TRANSLATION_THING_COMMANDS[intent]:
				## Si se encuentra el intent en la frase
				if synonymous in phrase:
					## Retornamos el intent a ejecutar
					return intent

		## Retornamos el objeto
		return None

	## Método que busca un dispositivo en la lista de dispositivos
	def match_ambience(self, phrase):
		## Recorremos la lista de dispositivos
		for ambience in self.melissa.things["ambiences"]:
			## Si se encuentra el dispositivo en la frase
			if ambience in phrase:
				## Retornamos el nombre del dispositivo
				return ambience

		## Retornamos el objeto
		return None

	###### Métodos que operan con Dispositivos ( Devices )
	## Método que busca un intent de dispositivo en una frase
	def match_device_intent(self, device, phrase):
		## Eliminamos Articulos y preposicones de la frase
		phrase = self.clear_string(phrase, True, True)

		## Recorremos la lista de dispositivos
		for intent in self.melissa.things["devices"][device].intents:
			## Recorre cada uno de los sinonimos de traduccion
			for synonymous in TRANSLATIONS.TRANSLATION_THING_COMMANDS[intent]:
				## Si se encuentra el intent en la frase
				if synonymous in phrase:
					## Retornamos el intent a ejecutar
					return intent

		## Retornamos el objeto
		return None

	## Método que busca un dispositivo en la lista de dispositivos
	def match_device(self, phrase):
		## Recorremos la lista de dispositivos
		for device in self.melissa.things["devices"]:
			## Si se encuentra el dispositivo en la frase
			if device in phrase:
				## Retornamos el nombre del dispositivo
				return device

		## Retornamos el objeto
		return None

	###### Métodos de utilidad
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