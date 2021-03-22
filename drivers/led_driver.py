## Importación de modulos necesarios
import drivers.led_library.apa102 as apa102
import time
import threading
from gpiozero import LED
try:
    import queue as Queue
except ImportError:
    import Queue as Queue
## Importación de patrones
from drivers.led_library.alexa_led_pattern import AlexaLedPattern as AlexaLedPattern
from drivers.led_library.google_home_led_pattern import GoogleHomeLedPattern as GoogleHomeLedPattern
from drivers.led_library.melissa_led_pattern import MelissaLedPattern as MelissaLedPattern

class Pixels:
    ## Constante que define la cantidad de LEDs del anillo
    PIXELS_N = 12
    
    ## Constructor
    def __init__(self, pattern=MelissaLedPattern, ledCount=12):
        self.PIXELS_N = ledCount
        self.dev = apa102.APA102(num_led=self.PIXELS_N)

        self.pattern = pattern(show=self.show)

        self.power = LED(5)
        self.power.on()

        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

        self.last_direction = None

    ## Método que fija un color
    def SetRingColorRGB(self, r, g, b):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, r, g, b)

        self.dev.show()

    ## Animación despertar
    def wakeup(self, direction=0):
        self.last_direction = direction
        def f():
            self.pattern.wakeup(direction)

        self.put(f)

    ## Animación escuchar
    def listen(self):
        if self.last_direction:
            def f():
                self.pattern.wakeup(self.last_direction)
            self.put(f)
        else:
            self.put(self.pattern.listen)

    ## Animación Pensar
    def think(self):
        self.put(self.pattern.think)

    ## Animación Hablar
    def speak(self):
        self.put(self.pattern.speak)

    ## Apagar
    def off(self):
        self.put(self.pattern.off)

    ## Métopdo privado que se usa para aplicar diseños sin patrón
    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)

    ## Método privado que ejecuta diseños sin patron
    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()

    ## Método privado que ordena a los led encenderse según el patron definido
    def show(self, data):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(data[4*i + 1]), int(data[4*i + 2]), int(data[4*i + 3]))

        self.dev.show()
