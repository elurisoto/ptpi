import pygame
import random

NEGRO = (0, 0, 0)
BLANCO = (255,255,255)
AZUL = (0,0,255)
VERDE = (0,255,0)
ROJO = (255,0,0)
MORADO = (255,0,255)
ancho_pantalla = 400
alto_pantalla = 600

class Jugador:
    x = 170
    y = 500
    ancho = 60
    alto = 60
    color = (68,184,172)

    def __init__(self):
        self = self

    def controles(self, pressed):
        if pressed[pygame.K_LEFT]: 
            if self.x > 0:
                self.x -= 3
        if pressed[pygame.K_RIGHT]: 
            if self.x < ancho_pantalla - self.ancho:
                self.x += 3


    def dibuja(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.ancho, self.alto))

class Enemigo:

    x = 0
    y = 0
    ancho = 10
    alto = 10
    velocidad = 1
    color = ROJO

    def __init__(self, x, y, alto, ancho, velocidad, color):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.color = color
        self.alto = alto
        self.ancho = ancho

    def movimiento(self):
        self.y += self.velocidad

    def dibuja(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.ancho, self.alto))
