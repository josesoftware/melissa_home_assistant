#######################################################################
## Objeto que representa un ambiente					             ##
#######################################################################

## Importación de modulos necesarios
import json
from objects import Thing

## Clase que representa un Ambiente
class Ambience(Thing):
	## Variables de estado
	lastColor = None

	## Constante que define el tamaño de un salto de intensidad
	INTENSITY_JUMP = 0.1

	## Atributos de estado
	color = "#000000"
	intensity = 1.0
	volume = 100

	## Constructor
	def __init__(self, name, color="#000000", intensity=1.0, volume=100):
		## Construimos el objeto padre
		Thing.__init__(self)

		## Definimos el nombre del ambiente
		self.alias = name

		## Definimos la lista de intents
		self.init_intents()

	## Inicializamos intents con variables reales
	def init_intents(self):
		## Acciones disponibles
		self.intents = {
			"color set": { "intent": "object_method", "parameters": { "method": "led_color", "color": self.color } },
			"attenuate": { "intent": "object_method", "parameters": { "method": "led_intensity", "argument": "attenuate" } },
			"increase": { "intent": "object_method", "parameters": { "method": "led_intensity", "argument": "increase" } },
			"maximum": { "intent": "object_method", "parameters": { "method": "led_intensity", "argument": "maximum" } },
			"minimum": { "intent": "object_method", "parameters": { "method": "led_intensity", "argument": "minimum" } },
			"volume up": { "intent": "object_method", "parameters": { "method": "audio_volume", "argument": "up" } },
			"volume down": { "intent": "object_method", "parameters": { "method": "audio_volume", "argument": "down" } },
			"volume max": { "intent": "object_method", "parameters": { "method": "audio_volume", "argument": "maximum" } },
			"volume min": { "intent": "object_method", "parameters": { "method": "audio_volume", "argument": "minimum" } }
		}

	## Método que ejecuta un intent
	def do_intent(self, intent):
		## Definimos una variable de retorno
		returnVar = None

		## Recupera los datos del intent como diccionario
		intentDictionary = json.loads(intent)

		## Si el intent es de tipo "object_method"
		if intentDictionary["intent"] == "object_method":
			## Determinamos que methodo se desea aplicar
			if intentDictionary["parameters"]["method"] == "led_color":
				## Definicion de color
				returnVar = self.color_set(intentDictionary["parameters"]["color"])

			elif intentDictionary["parameters"]["method"] == "led_intensity":
				## Definicion de intensidad
				returnVar = self.intensity_set(intentDictionary["parameters"]["argument"])

		## Retorna el returnVar
		return returnVar

	## Método que cambia el color del ambiente
	def color_set(self, newColor):
		## Fijemos el color
		self.color = newColor

		## Retorna el color
		return self.color

	## Método que atenua la intensidad del ambiente
	def intensity_set(self, argument):
		## Si se desea atenuar la intensidad
		if argument == "attenuate":
			## Si la intensidad es superior al salto de intensidad
			if self.intensity > self.INTENSITY_JUMP:
				## Atenuamos la intensidad 
				self.intensity = self.intensity - self.INTENSITY_JUMP
		elif argument == "increase":
			## Si la intensidad es menor o inferior al maximo menos el salto de intensidad
			if self.intensity <= (1.0 - self.INTENSITY_JUMP):
				## Incrementamos la intensidad 
				self.intensity = self.intensity - self.INTENSITY_JUMP
		elif argument == "maximum":
			## Incrementa la intensidad al maximo
			self.intensity = 1.0
		else:
			## Fija la intensidad al minimo valor
			self.intensity = self.INTENSITY_JUMP

		## Retorna la intensidad
		return self.intensity