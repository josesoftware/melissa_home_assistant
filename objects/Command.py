#######################################################################
## Objeto que representa un comando 	                             ##
#######################################################################

## Importa objeto padre
from objects import Thing

## Definicion del objeto
class Command(Thing):
    
    ## Constructor
    def __init__(self, alias):
        ## Inicializa el objeto padre
        Thing.__init__(self)

        ## Fija el nombre del comando
        self.alias = alias