#######################################################################
## Este driver se encarga de controlar el audio                      ##
#######################################################################

## Módulos necesarios
import pyaudio

class AudioDriver:
	## Constantes del modulo de audio
	READ_BUFFER = 1024
	READ_RATE = 16000
	WRITE_RATE = 44000
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
		self.inputStream = self.pyAudio.open(format=pyaudio.paInt16, channels=hardware.INPUT_AUDIO_CHANNELS, rate=self.READ_RATE, input=True, frames_per_buffer=self.READ_BUFFER)
		self.inputStream.start_stream()

		## Inicializamos el stream de output
		self.outputStream = self.pyAudio.open(format=pyaudio.paInt16, channels=hardware.OUTPUT_AUDIO_CHANNELS, rate=self.WRITE_RATE, output=True)
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
		return self.inputStream.read(self.READ_BUFFER)

	## Método que escribe en el stream de audio outpu
	def write(self, data):
		## Escribe en el buffer de salida
		self.outputStream.write(data)
    