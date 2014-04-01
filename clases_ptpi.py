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

screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))


class Jugador:
    x = 170
    y = 500
    ancho = 60
    alto = 60
    color = (68,184,172)

    def __init__(self):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def controles(self, pressed):
        if pressed[pygame.K_LEFT]: 
            if self.rect.x > 0:
                self.rect.x -= 3
        if pressed[pygame.K_RIGHT]: 
            if self.rect.x < ancho_pantalla - self.ancho:
                self.rect.x += 3


    def dibuja(self):
        pygame.draw.rect(screen, self.color, self.rect)

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
        self.rect = pygame.Rect(x, y, ancho, alto)

    def movimiento(self):
        self.rect.y += self.velocidad

    def dibuja(self):
        pygame.draw.rect(screen, self.color, self.rect)
