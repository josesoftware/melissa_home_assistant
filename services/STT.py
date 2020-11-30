###########################################################
## Servicio que se dedica a traducir voz en texto        ##
##-------------------------------------------------------##
## Basado en el STT PocketSphinx no requiere internet    ##
###########################################################

## Importacion de modulos necesarios
import os
from pocketsphinx import LiveSpeech, get_model_path

## Definición de la clase
class STTService:
    ## Servicio Sphinx
    SphinxService = None

    ## Instancia del servicio melissa
    Melissa = None

    ## Configuracion del Servicio STT
    SAMPLE_RATE = 20000 # Hz
    BUFFER_SIZE = 1024

    ## Constructor
    def __init__(self, melissaService):
        ## Instanciamos el servicio de IoT
        self.Melissa = melissaService

    ## Método que arranca el LiveSpeech de PocketSphinx
    def Start(self):
        ## Inicializamos el serivio Sphinx
        self.SphinxService = LiveSpeech(
            lm = False,
            verbose = True,
            sampling_rate = self.SAMPLE_RATE,
            buffer_size = self.BUFFER_SIZE,
            no_search = False,
            full_utt = False,
            hmm = os.path.join(get_model_path(), self.Melissa.Language["stt_model"]),
            #lm = os.path.join(model_path, 'es-20k.lm.bin'), ## Para detectar todo tipo de palabras en castellano
            kws = os.path.join(os.path.dirname(__file__), 'STT_Components/', self.Melissa.Language["keywords_file"] + '.list'),
            dict = os.path.join(os.path.dirname(__file__), 'STT_Components/', self.Melissa.Language["keywords_file"] + '.dict')
        )

        ## Mensaje de inicio
        print("Speech recognition starts")

        ## Recorremos las frases que detecta el sistema LiveSpeech
        for phrase in self.SphinxService:
            ## Invocamos al metodo ReadSTT del servicio de IoT
            self.Melissa.NLU.FromSTT(phrase.hypothesis())