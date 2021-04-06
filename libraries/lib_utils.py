##########################################################
## Librería que incluye funciones útiles de uso general ##
##########################################################

## Importamos modulos necesarios
import re, hashlib

## Método que combina una matriz eliminando elementos duplicados
def merge_array(array):
	## Matríz de retorno
	result = []

	## Recorre cada elemento del array
	for element in array:
		## Si el elemanto no está incluido en el array resultante
		if element not in result:
			## Agregamos el elemento al array resultante
			result.append(element)

	## Retorna el resultado
	return result

## Método que delimita el valor de un integer
def int_clamp(value, minVal, maxVal):
	return max(min(value, maxVal), minVal)

## Método que encripta en MD5 un string
def string_to_md5(inString):
	## Generamos un hash del nombre "unknown"
	hash_obj = hashlib.md5(inString)

	## Retorna la cadena MD5
	return hash_obj.hexdigest()

## Método que cuenta palabras de un string
def count_words(inString):
	## Retorna el recuento de palabras
	return len(inString.split())

## Métodoo que reemplaza un caracter de un string por otro
def replace_char(inString, oldChar, newChar):
	## Retorna el string modificando los caracteres deseados
	return inString.replace(oldChar, newChar)

## Método que reliza un split con multiples delimitadores
def multi_split(inString, delimitterList):
	## Definimos primero el string de delimitadores
	delimitters = ""

	## Recorremos la lista de delimitadores
	for delimitter in delimitterList:
		## Reconstruimos la lista de delimitadores
		if len(delimitters) > 0: ## Si ya se ha añadido un delimitador
			## Concatenamos el string con un separador
			delimitters = delimitters + "|" + delimitter
		else:
			## Asignamos directamente el delimitador
			delimitters = delimitter

	## Retornamos el array resultante
	return re.split(delimitters, inString)