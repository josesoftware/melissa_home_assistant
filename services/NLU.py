###############################################################
## Componente que se dedica a comprender un lenguaje natural ##
##-----------------------------------------------------------##
## Convierte textos de un lenguaje natural en Intents        ##
###############################################################

## Definición del objeto
class NLUService:
    ## Instancia del servicio de IoT
    MelissaService = None

    ## Constructor
    def __init__(self, melissaService):
        ## Instanciamos el servicio Melissa
        self.MelissaService = melissaService

    ## Método que recibe datos del servicio STT
    def FromSTT(self, sttInput):
        print(sttInput)