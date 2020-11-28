#################################################################
## Objeto que representa el servicio de IoT 				   ##
#################################################################

## Clase
class MelissaService:
	#### Atributos estaticos
	## Idicador de estado
	WakeUp = False
	## Indicador de bloqueo
	Locked = False
	## Instancia del modulo LED
	LED_Module = None

	## Constructor
	def __init__(self, LED_Module):
		## Instanciamos el módulo LED
		self.LED_Module = LED_Module

	## Método que despierta al servicio
	def Wake(self):
		## Modificamos la valiza de estado
		self.WakeUp = True

		## Animamos los led con la animacion de despertar
		if self.LED_Module is not None:
			self.LED_Module.wakeup()

		## Mensaje de aviso
		print("Melissa is wake up")

	## Método que duerme al servicio
	def Sleep(self):
		## Modificamos la valiza de estado
		self.WakeUp = False

		## Apagamos los led
		if self.LED_Module is not None:
			self.LED_Module.off()

		## Mensaje de aviso
		print("Melissa is sleeping")

	## Método que aborta el servicio
	def Abort(self):
		## Modificamos la valiza de estado
		self.WakeUp = False

		## Apagamos los led
		if self.LED_Module is not None:
			self.LED_Module.off()

		## Mensaje de aviso
		print("See you soon!")
		
		## Salimos de la APP
		quit()