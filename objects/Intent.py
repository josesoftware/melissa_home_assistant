#######################################################################
## Objeto que representa un intent ( Intención )					 ##
#######################################################################

## Clase del objeto
class Intent():
    ## Atributo que representa el tipo de acción que se prentende con este Intent
    Action = None

    ## Atributo que representa parámetros adicionales a la acción que se pretende
    Parameters = {} 

    ## Constructor
    def __init__(self, action):
        ## Definimos acción
        self.Action = action
        
    ## Método que añade un parametro al intent
    def AddParam(self, param, value):
        ## Añadimos el parametro a la lista
        self.Parameters[param] = value