##########################################################
## Librería que incluye funciones útiles de uso general ##
##########################################################

## Importamos modulos necesarios
import re

## Método que cuenta palabras de un string
def CountWords(inString):
	## Retorna el recuento de palabras
	return len(inString.split())

## Método que reliza un split con multiples delimitadores
def MultiSplit(inString, delimitterList):
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