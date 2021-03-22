#!/usr/bin/env python

# Copyright (C) 2017 Seeed Technology Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import numpy
import time
 
class MelissaLedPattern(object):
    def __init__(self, show=None, number=12):
        self.pixels_number = number
        self.pixels = [0] * 4 * number

        if not show or not callable(show):
            def dummy(data):
                pass
            show = dummy

        self.show = show
        self.stop = False

    def wheel(self, wheel_pos):
        """Get a color from a color wheel; Green -> Red -> Blue -> Green"""

        if wheel_pos > 255:
            wheel_pos = 255 # Safeguard
        if wheel_pos < 85:  # Green -> Red
            return [wheel_pos * 3, 255 - wheel_pos * 3, 0]
        if wheel_pos < 170:  # Red -> Blue
            wheel_pos -= 85
            return [255 - wheel_pos * 3, 0, wheel_pos * 3]
        # Blue -> Green
        wheel_pos -= 170
        return [0, wheel_pos * 3, 255 - wheel_pos * 3]

    ## Animación estilo transición de colores
    def rainbow(self, wait_ms=20):
        ## Seteamos el valor inicial
        pixels = [0, 0, 0, 0] * self.pixels_number
        
        ## Declaramos un contador
        j = 0
        
        ## Efecto de transicion de color
        while not self.stop:
            ## Recorremos cada uno de los led
            for i in range(self.pixels_number):
                ## Calculamos el wheel
                wheel = self.wheel((i+j) & 255)

                ## Fijamos el color RGB
                pixels[i * 4 + 1] = wheel[0]
                pixels[i * 4 + 2] = wheel[1]
                pixels[i * 4 + 3] = wheel[2]
                
            ## Mostramos pixeles
            self.show(pixels)
                
            ## Tiempo de espera entre ciclos
            time.sleep(wait_ms/1000.0)
                
            ## Incrementamos el contador    
            j += 1
            
    ## Animación estilo transición de colores
    def rainbowCycle(self, wait_ms=20):
        ## Seteamos el valor inicial
        pixels = [0, 0, 0, 0] * self.pixels_number
        
        ## Declaramos un contador
        j = 0
        
        ## Efecto de transicion de color
        while not self.stop:
        
            ## Recorremos cada uno de los led
            for i in range(self.pixels_number):
                ## Calculamos el wheel
                wheel = self.wheel((int(i * 256 / self.pixels_number) + j) & 255)

                ## Fijamos el color RGB
                pixels[i * 4 + 1] = wheel[0]
                pixels[i * 4 + 2] = wheel[1]
                pixels[i * 4 + 3] = wheel[2]
                
            ## Mostramos pixeles
            self.show(pixels)
                
            ## Tiempo de espera entre ciclos
            time.sleep(wait_ms/1000.0)
                
            ## Incrementamos el contador    
            j += 1

    ## Animacion de despertar
    def simplewakeup(self, direction=0):
        ## Determinamos el led mas proximo a la voz
        position = int((direction + 15) / (360 / self.pixels_number)) % self.pixels_number
        
        ## Seteamos el valor inicial
        pixels = [0, 0, 0, 0] * self.pixels_number
        
        ## Recorremos cada uno de los led
        for i in range(self.pixels_number):
            ## Calculamos el wheel
            wheel = self.wheel(int(i * 256 / self.pixels_number) & 255)

            ## Fijamos el color RGB
            pixels[i * 4 + 1] = wheel[0]
            pixels[i * 4 + 2] = wheel[1]
            pixels[i * 4 + 3] = wheel[2]

        ## Mostramos color
        self.show(pixels)

    ## Animacion de despertar
    def wakeup(self, direction=0):
        ## Determinamos el led mas proximo a la voz
        #position = int((direction + 15) / (360 / self.pixels_number)) % self.pixels_number
        
        ## Seteamos el valor inicial
        pixels = [0, 0, 0, 0] * self.pixels_number
        
        ## Aplicamos animacion fade
        for o in range(100):
            ## Recorremos cada uno de los led
            for i in range(self.pixels_number):
                ## Calculamos el wheel
                wheel = self.wheel(int(i * 256 / self.pixels_number) & 255)
            
                #if i != position:
                #    ## Fijamos el color RGB
                #    pixels[i * 4 + 1] = wheel[0] * 0.5
                #    pixels[i * 4 + 2] = wheel[1] * 0.5
                #    pixels[i * 4 + 3] = wheel[2] * 0.5
                #else:
                ## Fijamos el color RGB
                pixels[i * 4 + 1] = wheel[0] * (0.01 * o)
                pixels[i * 4 + 2] = wheel[1] * (0.01 * o)
                pixels[i * 4 + 3] = wheel[2] * (0.01 * o)
            
            ## Duerme 0,001s
            time.sleep(0.001)

            ## Mostramos color
            self.show(pixels)

    ## Animacion de escuchar
    def listen(self):
        ## Seteamos el valor inicial
        pixels = [0, 0, 0, 0] * self.pixels_number
        
        ## Recorremos cada uno de los led
        for i in range(self.pixels_number):
            ## Calculamos el wheel
            wheel = self.wheel(int(i * 256 / self.pixels_number) & 255)

            ## Fijamos el color RGB
            pixels[i * 4 + 1] = wheel[0] * 0.85
            pixels[i * 4 + 2] = wheel[1] * 0.85
            pixels[i * 4 + 3] = wheel[2] * 0.85

        ## Mostramos color
        self.show(pixels)

    ## Animacion de pensar
    def think(self):
        ## Tiempo de espera de la animacion
        wait_ms = 20
        
        ## Seteamos el valor inicial
        pixels = [0, 0, 0, 0] * self.pixels_number
        
        ## Declaramos un contador
        j = 0
        
        ## Efecto de transicion de color
        while not self.stop:
            ## Recorremos cada uno de los led
            for i in range(self.pixels_number):
                ## Calculamos el wheel
                wheel = self.wheel((i+j) & 255)

                ## Fijamos el color RGB
                pixels[i * 4 + 1] = wheel[0]
                pixels[i * 4 + 2] = wheel[1]
                pixels[i * 4 + 3] = wheel[2]
                
            ## Mostramos pixeles
            self.show(pixels)
                
            ## Tiempo de espera entre ciclos
            time.sleep(wait_ms / 1000.0)
                
            ## Incrementamos el contador    
            j += 1

    ## Animacion de hablar
    def speak(self):
        ## Tiempo de espera de la animacion
        wait_ms=10
    
        ## Seteamos el valor inicial
        pixels = [0, 0, 0, 0] * self.pixels_number
        
        ## Declaramos un contador
        j = 0
        
        ## Efecto de transicion de color
        while not self.stop:
        
            ## Recorremos cada uno de los led
            for i in range(self.pixels_number):
                ## Calculamos el wheel
                wheel = self.wheel((int(i * 256 / self.pixels_number) + j) & 255)

                ## Fijamos el color RGB
                pixels[i * 4 + 1] = wheel[0]
                pixels[i * 4 + 2] = wheel[1]
                pixels[i * 4 + 3] = wheel[2]
                
            ## Mostramos pixeles
            self.show(pixels)
                
            ## Tiempo de espera entre ciclos
            time.sleep(wait_ms/1000.0)
                
            ## Incrementamos el contador    
            j += 1

    ## Animacion para apagar leds
    def off(self):
        self.show([0] * 4 * 12)
