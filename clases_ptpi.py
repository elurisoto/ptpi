import pygame
import random
from ssheet import *


NEGRO = (0, 0, 0)
BLANCO = (255,255,255)
AZUL = (0,0,255)
VERDE = (0,255,0)
ROJO = (255,0,0)
MORADO = (255,0,255)
ancho_pantalla = 400
alto_pantalla = 600


screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
#screen = pygame.Surface((ancho_pantalla, alto_pantalla), pygame.SRCALPHA)
#screen.set_colorkey((0,67,171))
screen.set_alpha()

ss = spritesheet("1945.png")
sprites = pygame.sprite.LayeredUpdates()

class Jugador(pygame.sprite.Sprite):
	x = 170
	y = 500
	ancho = 60
	alto = 60
	color = (68,184,172)
	radius = 30
	layer = 0

	def __init__(self):
		self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
		pygame.sprite.Sprite.__init__(self)
		self.image = ss.image_at((301,235,65,65),(0,67,171))
		sprites.add(self)


	def update(self, pressed):
		if pressed[pygame.K_LEFT]: 
			if self.rect.x > 0:
				self.rect.move_ip(-3, 0)
		if pressed[pygame.K_RIGHT]: 
			if self.rect.x < ancho_pantalla - self.ancho:
				self.rect.move_ip(3, 0)


class Enemigo(pygame.sprite.Sprite):

	x = 0
	y = 0
	ancho = 30
	alto = 30
	velocidad = 1
	color = ROJO
	radius = 10
	layer = 0

	def __init__(self, x, y, alto, ancho, velocidad, color):
		self.x = x
		self.y = y
		self.velocidad = velocidad
		self.color = color
		self.alto = alto
		self.ancho = ancho
		self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
		pygame.sprite.Sprite.__init__(self)
		self.image = ss.image_at((5,5,30,30),(0,67,171))
		sprites.add(self)

	def update(self):
		self.rect.y += self.velocidad

