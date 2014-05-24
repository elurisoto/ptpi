#-*-coding:utf-8-*-

from ia import *
from clases_ptpi import *
from ssheet import *
from sstripanim import *
from copy import copy
import pyganim

def matar(enemigo):
	enemigo.kill()
	i = enemigos.index(enemigo)
	for j in range(len(enemigos_h)):
		if enemigos_h[j][1] == i:
			del(enemigos_h[j])
			break
	if enemigo in enemigos:
		enemigos.remove(enemigo)

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
			matar(enem)
			

		for disp in disparos:
			if pygame.sprite.collide_circle(disp, enem):
				explotar = True
				posicionexplosion = (enem.rect.x, enem.rect.y)
				explosion.play()
				#enem.kill()
				disp.kill()
				#if enem in enemigos:
				#	enemigos.remove(enem)
				matar(enem)
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
# lista especial de enemigos en la que en el momento que se dispara a un enemigo este se borra, sin esperar a la colisión
enemigos_h = []		
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
				enemigos_h.append([[e_x + enemigos[0].ancho/2,e_y + enemigos[0].alto/2], len(enemigos)-1])
				t_enemigo = pygame.time.get_ticks()



			colisiones(enemigos, jugador, disparos)

			# Si quito el +10 todo deja de funcionar, NI ZORRA DE POR QUÉ
			e = Estado(puntos, [jugador.rect.x + jugador.ancho/2 +10, jugador.rect.y + jugador.alto/2], enemigos_h, jugador.velocidad)
			l = busqueda_profundidad(e,0)
			mov = l.index(max(l))
			if max(l[0]) == max(l[1]) == max(l[2]):
				mov = NADA

			#print max(l)

			# if mov == DISPARAR:
			# 	for i in enemigos_h:	#Cálculos para ver si en caso de disparar habría colisión
			# 		if i[0] - 6 <= jugador.rect.x + jugador.ancho/2  <= i[0]+6:
			# 			#print "hit"
			# 			enemigos_h.remove(i)
			# 			break
			# 	else:
			# 		mov = NADA
			# 		print "NADA"

			jugador.control(mov)


			# for i,e in enumerate(enemigos_h):
			# 	enemigos_h[i][1]+=1

			# 	if e[1] > alto_pantalla:
			# 		enemigos_h.remove(e)

			if explotar:
				explosion.blit(screen, posicionexplosion)

			if explosion.state == pyganim.STOPPED:
				explotar = False
				explosion.stop()

			for i, e in enumerate(enemigos):
				if e.rect.y > alto_pantalla + 10:
					matar(e)

			for i, d in enumerate(disparos):
				if d.rect.y < -10:
					d.kill()
					del disparos[i]

			for i,isla in enumerate(islas):
				if isla.rect.y > alto_pantalla + 20:
					isla.kill()
					del islas[i]

			clock.tick(60)

		pygame.display.flip()



