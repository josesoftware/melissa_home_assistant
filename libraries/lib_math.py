###############################################################################################
# Librería que alberga funciones de cálculos matemáticos controlados y utilidades matemáticas #
###############################################################################################

# Método controla el valor máximo y mínimo que se le puede asignar a un número entero
def IntClamp(inputVal, minVal, maxVal):
	# Calculamos el resultado
	result = max(min(int(inputVal), int(maxVal)), int(minVal))
	
	# Retornamos el valor recortado a los límites facilitados por argumento
	return result
	
# Método realiza una división segura
def Divide(dividend, divider):
	# Controlamos que el valor del divisor sea válido
	if divider == 0: divider = 1

	# Retornamos el valor recortado a los límites facilitados por argumento
	return dividend / divider