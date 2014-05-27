#-*-coding:utf-8-*-

import pygame
import random
from ssheet import *


NEGRO = (0, 0, 0)
BLANCO = (255,255,255)
AZUL = (0,0,255)
VERDE = (0,255,0)
ROJO = (255,0,0)
MORADO = (255,0,255)
ancho_pantalla = 600
alto_pantalla = 600
ancho_enemigo = 30
alto_enemigo = 30

IZQUIERDA = 0
DERECHA = 1
DISPARAR = 2
NADA = 3


screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
screen.set_alpha()
disparos = []

ss = spritesheet("1945.png")
sprites = pygame.sprite.LayeredUpdates()

class Jugador(pygame.sprite.Sprite):
	x = ancho_pantalla/2
	y = 500
	ancho = 60
	alto = 60
	velocidad = 3
	radius = 30
	_layer = 1
	ultimodisparo = 0
	temporizador_disparos = 80

	def __init__(self):
		self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
		pygame.sprite.Sprite.__init__(self)
		self.image = ss.image_at((301,235,65,65),(0,67,171))
		sprites.add(self)


	def update(self, pressed):
		movx = 0

		if pressed[pygame.K_LEFT]: 
			if self.rect.x > 0:
				movx = -self.velocidad
		if pressed[pygame.K_RIGHT]: 
			if self.rect.x < ancho_pantalla - self.ancho:
				movx = self.velocidad

		self.rect.move_ip(movx, 0)

		if pressed[pygame.K_SPACE]:
			self.dispara()

	def dispara(self):
		if pygame.time.get_ticks() - self.ultimodisparo >= self.temporizador_disparos:

			disparos.append(Disparo(self.rect.x+17, self.rect.y-15, 5))
			self.ultimodisparo = pygame.time.get_ticks()

	def control(self, orden):
		movx = 0

		if orden == IZQUIERDA:
			if self.rect.x > -self.ancho/2:
				movx = -self.velocidad
		elif orden == DERECHA:
			if self.rect.x < ancho_pantalla + self.ancho+10:
				movx = self.velocidad
		elif orden == DISPARAR:
			self.dispara()


		self.rect.move_ip(movx, 0)




class Enemigo(pygame.sprite.Sprite):

	x = 0
	y = 0
	ancho = 30
	alto = 30
	velocidad = 1
	color = ROJO
	radius = 10
	_layer = 1


	def __init__(self, x, y, alto, ancho, velocidad, color):
		self.x = x
		self.y = y
		self.velocidad = velocidad
		self.color = color
		self.alto = alto
		self.ancho = ancho
		self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
		pygame.sprite.Sprite.__init__(self)
		self.image = ss.image_at((5,5,31,31),(0,67,171))
		sprites.add(self)

	def update(self, pressed):
		self.rect.y += self.velocidad


class Disparo(pygame.sprite.Sprite):

	radius = 5
	_layer = 1

	def __init__(self, x, y, velocidad):
		self.x = x
		self.y = y
		self.velocidad = velocidad

		self.rect = pygame.Rect(self.x, self.y, 31, 31)
		pygame.sprite.Sprite.__init__(self)
		self.image = ss.image_at((37, 170, 31, 31), (0, 67, 171))
		sprites.add(self)

	def update(self,pressed):
		self.rect.y -= self.velocidad



class Isla(pygame.sprite.Sprite):
	_layer = 0
	y = -70
	velocidad = 1
	_mover = 0
	def __init__(self,x,indicesprite):
		self.x = x
		self.rect = pygame.Rect(self.x, self.y, 62,62)
		pygame.sprite.Sprite.__init__(self)

		if indicesprite == 0:
			self.image = ss.image_at((105,500, 62,62), (0,67,171))
		elif indicesprite == 1:
			self.image = ss.image_at((168,500,62,62), (0,67,171))
		elif indicesprite == 2:
			self.image = ss.image_at((233,500,62,62), (0,67,171))

		sprites.add(self)
	def update(self, pressed):
		if self._mover == 0:
			self.rect.y += self.velocidad
		self._mover = (self._mover + 1)%3





