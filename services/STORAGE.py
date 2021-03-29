#######################################################################
## Este servicio se encarga del control de ficheros y directorios    ##
#######################################################################

## Importacion de módulos
import os, json, datetime, shutil, pathlib

## Importación de librerías
from libraries.lib_utils import string_to_md5

## Clase que representa al objeto Storage Driver
class StorageService:
	## Constantes
	ROOT_DIR = "/var/melissa/"
	CONFIG_FILENAME = "bee.json"
	LOG_DIR = "log/"

	## Instancia del servicio melissa
	melissa = None

	## Constructor
	def __init__(self, melissaService):
		## Instancia el servicio melissa
		self.melissa = melissaService

	## Método que comprueba si existe el fichero de configuración
	def check_configfile_exists(self):
		## Controla excepciones
		try:
			f = open(os.path.join(self.ROOT_DIR, self.CONFIG_FILENAME))
			f.close()
			## Retorna true si todo ha ido bien
			return True
		except IOError:
			## Retorna falso si hay error
			return False

	## Método que carga el contenido del fichero de configuración
	def load_configfile(self):
		## Declaramos variable de retorno
		returnJson = None

		## Si no existe el fichero, retornará nulo
		if not self.check_configfile_exists():
			return returnJson

		## Controla excepciones
		try:
			## Abre el fichero de configuración para leerlo
			f = open(os.path.join(self.ROOT_DIR, self.CONFIG_FILENAME), 'r')
			returnJson = json.loads(f.read())
			## Cierra el fichero de configuración
			f.close()
		except IOError:
			## Cuando hay un error cargando el fichero
			self.log_debug_write('Configuration file unaccesible', 'IO Error')
		except ValueError:
			## Cuando hay un error decodificando el JSON
			self.log_debug_write('Bad JSON format on configuration file', 'Decoding Error')
		except:
			## Cuando hay un error genérico
			self.log_debug_write('General error writen the configuration file', 'IO Error')

		## Retorna la configuración
		return returnJson

	## Método que crea o modifica el fichero de configuración
	def write_configfile(self, configDictionary):
		## Controla excepciones
		try:
			## Abre el fichero de configuración para sobreescribirlo
			f = open(os.path.join(self.ROOT_DIR, self.CONFIG_FILENAME), 'w')
			
			## Escribe el diccionario de configuración en el fichero codificandolo como JSON
			f.write(json.dumps(configDictionary, indent=4))
		except IOError:
			## Cuando hay un error cargando el fichero
			self.log_debug_write('Configuration file unaccesible', 'IO Error')
		except:
			## Cuando hay un error genérico
			self.log_debug_write('General error writen the configuration file', 'IO Error')

	## Método que devuelve el hostname de la máquina
	def get_machine_hostname(self):
		## Control de excepciones
		try:
			## Recupera datos de ficheros
			hostnameFile = open("/etc/hostname", "r")
			hostname = hostnameFile.read()
			## Cierre de ficheros
			hostnameFile.close()

			## Retornará el hostname obtenido
			return hostname
		except:
			return "unknown"

	## Método que devuelve el machine-id de la máquina
	def get_machine_id(self):
		## Control de excepciones
		try:
			## Recupera datos de ficheros
			machineIdFile = open("/etc/hostname", "r")
			machjineId = machineIdFile.read()
			## Cierre de ficheros
			machineIdFile.close()

			## Retornará el hostname obtenido
			return machjineId
		except:
			## Generamos un hash del nombre "unknown"
			return string_to_md5(b'unknown')


	################################# Métodos del LOG
	## Método que crea el directorio logs si no existe
	def make_log_dir(self):
		## Define el directorio
		folder = os.path.join(self.ROOT_DIR, self.LOG_DIR)

		## Controla excepciones de IO
		try:
			## Si no existe el directorio
			if not os.path.exists(folder):
				## Crea el directorio
				os.makedirs(folder)

			## Retorna True si todo va bien
			return True
		except Exception as e:
			## Debug message
			print('ERROR: Failed creating the logs directory. Reason: %s' % (e))

			## Retorna False con cualquier error
			return False

	## Método que escribe una línea en el log
	def log_write(self, text, title):
		## Determina la fecha actual
		now = datetime.datetime.now()

		## Si el directorio existe
		if self.make_log_dir():
			## Controla excepciones para trabajar con ficheros
			try:
				## Abre el fichero de log para añadir una línea
				logfile = open(os.path.join(self.ROOT_DIR, self.LOG_DIR, now.strftime("%Y-%m-%d") + '_logfile'), 'a')

				## Escribe la línea en el log
				logfile.write(now.strftime("%Y-%m-%d %H:%M:%S") + '\t' + title + ': ' + text)

				## Cierra el fichero
				logfile.close()
			
			except Exception as e:
					## Debug message
					print('ERROR: Error writing in log file. Reason: %s' % (e))

	## Método que escribe una línea de debug en el log
	def log_debug_write(self, text, title):
		## Siempre que el servicio esté en modo debug
		if self.melissa.debugMode:
			## Determina la fecha actual
			now = datetime.datetime.now()

			## Si el directorio existe
			if self.make_log_dir():
				## Controla excepciones para trabajar con ficheros
				try:
					## Abre el fichero de log para añadir una línea
					logfile = open(os.path.join(self.ROOT_DIR, self.LOG_DIR, now.strftime("%Y-%m-%d") + '_debugfile'), 'a')

					## Escribe la línea en el log
					logfile.write(now.strftime("%Y-%m-%d %H:%M:%S") + '\t (Debug) ' + title + ': ' + text)

					## Cierra el fichero
					logfile.close()

				except Exception as e:
					## Debug message
					print('ERROR: Error writing in debug file. Reason: %s' % (e))

	## Método que purga el log
	def log_clear(self, limitDate=None):
		## Si el directorio existe
		if self.make_log_dir():
			## Define el path del directorio Logs
			folder = os.path.join(self.ROOT_DIR, self.LOG_DIR)

			## Controla excepciones
			try:
				## Purgará todo el log
				for filename in os.listdir(folder):
					## Recupera la URL del archivo
					file_path = os.path.join(folder, filename)

					## Si no se ha definido un límite de fecha para purgar
					if limitDate is None:
						## Controla excepciones
						try:
							## Si es un fichero lo elimina
							if os.path.isfile(file_path) or os.path.islink(file_path):
								os.unlink(file_path)

							## Si es un subdirectorio lo elimina a el y su contenido
							elif os.path.isdir(file_path):
								shutil.rmtree(file_path)

						except Exception as e:
							## Debug message
							print('ERROR: Failed to delete %s. Reason: %s' % (file_path, e))
					else:
						## Purgará los logs antiguos
						fname = pathlib.Path(file_path)

						## Recupra la fecha de modificación del archivo
						mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
						
						## Si la ultima modificación del fichero es anterior que la fecha límite, lo purgará
						if (limitDate < mtime):
							## Controla excepciones
							try:
								## Si es un fichero lo elimina
								if os.path.isfile(file_path) or os.path.islink(file_path):
									os.unlink(file_path)

								## Si es un subdirectorio lo elimina a el y su contenido
								elif os.path.isdir(file_path):
									shutil.rmtree(file_path)

							except Exception as e:
								## Debug message
								print('ERROR: Failed to delete %s. Reason: %s' % (file_path, e))

			except Exception as e:
				## Debug message
				print('ERROR: Failed to purge logs. Reason: %s' % (e))