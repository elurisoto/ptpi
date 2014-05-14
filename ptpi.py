#-*-coding:utf-8-*-

from ia import *
from clases_ptpi import *
from ssheet import *
from sstripanim import *
from copy import copy
import pyganim


def colisiones(enemigos, jugador, disparos):
	i = j = 0
	global explotar
	global posicionexplosion
	global marcador
	global puntos
	for enem in enemigos:
		if pygame.sprite.collide_circle(enem, jugador):
			explotar = True
			posicionexplosion = (enem.rect.x, enem.rect.y)
			explosion.play()
			enem.kill()
			enemigos.remove(enem)
			

		for disp in disparos:
			if pygame.sprite.collide_circle(disp, enem):
				explotar = True
				posicionexplosion = (enem.rect.x, enem.rect.y)
				explosion.play()
				enem.kill()
				disp.kill()
				if enem in enemigos:
					enemigos.remove(enem)
				disparos.remove(disp)
				puntos += 1
				marcador = myfont.render("SCORE: " + str(puntos), 0, (255,255,0))
					



def dibuja_fondo():

	fondo.image = ss.image_at((268,367,32,32))
	fondo.layer = 2

	for i in range(0,ancho_pantalla,32):
		for j in range(0,alto_pantalla,32):

			fondo.rect = pygame.Rect((i,j,32,32))
			sprites.add(copy(fondo)) 		#No me convence


pygame.init()

explosion = pyganim.PygAnimation([	('animaciones/explosion1.png',0.05),
									('animaciones/explosion2.png',0.05),
									('animaciones/explosion3.png',0.05),
									('animaciones/explosion4.png',0.05),
									('animaciones/explosion5.png',0.05),
									('animaciones/explosion6.png',0.05),
									('animaciones/explosion7.png',0.05),
								], loop = False)

explosion.set_colorkey((0,65,175))

done = False
enemigos = []
islas = []
explotar = False
puntos = 0

myfont = pygame.font.Font("fuente.ttf", 15)

# render text
marcador = myfont.render("SCORE: 0", 0, (255,255,0))


isla = Isla(random.randint(0,ancho_pantalla + 20), random.randint(0,2))
islas.append(isla)
ultimaisla = pygame.time.get_ticks()
proximaisla = random.uniform(2000, 5000) + pygame.time.get_ticks()

clock = pygame.time.Clock()
t_enemigo = pygame.time.get_ticks()
fondo = pygame.sprite.Sprite()

dibuja_fondo()
jugador = Jugador()
pause = False

while not done:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
						done = True
		
		pressed = pygame.key.get_pressed()

		if pressed[pygame.K_ESCAPE]: done = True

		if pressed[pygame.K_p]: pause = not pause

		if not pause:
			#screen.fill((0, 67, 171))
			screen.fill((0,0,0,0))
			# jugador.update(pressed)
			sprites.draw(screen)
			sprites.update(pressed)
			screen.blit(marcador, (10, 10))

			if pygame.time.get_ticks() - ultimaisla > proximaisla:
				ultimaisla = pygame.time.get_ticks()
				proximaisla = random.uniform(500, 1000) + pygame.time.get_ticks()
				isla = Isla(random.randint(0,ancho_pantalla + 20), random.randint(0,2))
				islas.append(isla)

			if pygame.time.get_ticks() - t_enemigo > 750:
				e_x = random.randint(5, ancho_pantalla-30)
				e_y = -10
				enemigos.append(Enemigo(e_x,e_y, 30, 30, 3, ROJO))
				t_enemigo = pygame.time.get_ticks()



			colisiones(enemigos, jugador, disparos)
			l = [i.rect.x + i.ancho/2 for i in enemigos]

			e = Estado(puntos, jugador.rect.x + jugador.ancho/2, l, jugador.velocidad)
			l = e.hijos()
			l = [i.evaluar() for i in l]
			mov = l.index(max(l))
			jugador.control(mov)

			#print e.evaluar()
			if explotar:
				explosion.blit(screen, posicionexplosion)
			if explosion.state == pyganim.STOPPED:
				explotar = False
				explosion.stop()

			for i, e in enumerate(enemigos):
				# e.update()

				if e.rect.y > alto_pantalla + 20:
					e.kill()
					del enemigos[i]


			for i, d in enumerate(disparos):
				# d.update()

				if d.rect.y < -10:
					d.kill()
					del disparos[i]

			for i,isla in enumerate(islas):
				# isla.update()
				if isla.rect.y > alto_pantalla + 20:
					isla.kill()
					del islas[i]
			clock.tick(60)


		pygame.display.flip()



