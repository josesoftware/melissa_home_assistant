#######################################################################
## Este driver se encarga de controlar el audio                      ##
#######################################################################

## Módulos necesarios
import pyaudio

class AudioDriver:
	## Constantes del modulo de audio
	READ_BUFFER = 8192
	WRITE_BUFFER = 1024

	## Instancia de pyAudio
	pyAudio = None

	## Streams
	inputStream = None
	outputStream = None

	## Constructor
	def __init__(self, hardware):
		## Inicializamos PyAudio
		self.pyAudio = pyaudio.PyAudio()

		## Inicializamos el stream de input
		self.inputStream = self.pyAudio.open(format=self.pyAudio.get_format_from_width(hardware.INPUT_AUDIO_WIDTH), channels=hardware.INPUT_AUDIO_CHANNELS, rate=hardware.INPUT_AUDIO_RATE, input=True, frames_per_buffer=self.READ_BUFFER)
		self.inputStream.start_stream()

		## Inicializamos el stream de output
		self.outputStream = self.pyAudio.open(format=pyaudio.paInt16, channels=hardware.OUTPUT_AUDIO_CHANNELS, rate=hardware.OUTPUT_AUDIO_RATE, output=True)
		self.outputStream.start_stream()

	## Destructor
	def __del__(self):
		## Cerramos los streams
		if self.inputStream is not None:
			self.inputStream.close()
		if self.outputStream is not None:
			self.outputStream.close()

		## Siempre exista una instancia
		if self.pyAudio is not None:
			## Terminamos el proceso PyAudio
			self.pyAudio.terminate()

	## Método que lee del stream de audio input
	def read(self):
		## Retorna el fragmento del stream usando el buffer
		if self.inputStream is not None:
			return self.inputStream.read(self.READ_BUFFER)
		else:
			return []

	## Método que escribe en el stream de audio outpu
	def write(self, data):
		## Escribe en el buffer de salida
		if self.outputStream is not None:
			self.outputStream.write(data)
    