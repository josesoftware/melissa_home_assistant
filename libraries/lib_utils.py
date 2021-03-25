##########################################################
## Librería que incluye funciones útiles de uso general ##
##########################################################

## Importamos modulos necesarios
import re

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

## Método que cuenta palabras de un string
def count_words(inString):
	## Retorna el recuento de palabras
	return len(inString.split())

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