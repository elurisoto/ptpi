#-*-coding:utf-8-*-
import sys
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
	global puntos
	global vidas

	for enem in enemigos:
		if pygame.sprite.collide_circle(enem[0], jugador):	# Busca colisiones enemigo-jugador
			explotar = True
			posicionexplosion = (enem[0].rect.x, enem[0].rect.y)
			explosion.play()
			enem[0].kill()
			enemigos.remove(enem)
			vidas -= 1
			

		for disp in disparos:	# Busca colisiones disparo-enemigo
			if pygame.sprite.collide_circle(disp, enem[0]):
				explotar = True
				posicionexplosion = (enem[0].rect.x, enem[0].rect.y)
				explosion.play()
				enem[0].kill()
				disp.kill()
				if enem in enemigos:
					enemigos.remove(enem)
				disparos.remove(disp)
				puntos += 5
					


# Llena el fondo del sprite del mar
def dibuja_fondo():

	fondo.image = ss.image_at((268,367,32,32))
	fondo.layer = 2

	for i in range(0,ancho_pantalla,32):
		for j in range(0,alto_pantalla,32):

			fondo.rect = pygame.Rect((i,j,32,32))
			sprites.add(copy(fondo)) 		#No me convence


pygame.init()

# Carga la animación de las explosiones
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

# La estructura de enemigos es: [Objeto de la clase enemigo, posición real del mismo, booleano que indica si ya se le ha disparado]
enemigos = []
islas = []
explotar = False
puntos = 0
vidas = 3
manual = False


if len(sys.argv) >1:
	manual = sys.argv[1] == "-m"

myfont = pygame.font.Font("fuente.ttf", 15)
marcador = myfont.render("SCORE: 0", 0, (255,255,0))
marcavidas = myfont.render("PLANES: 3", 0, (255,255,0))

isla = Isla(random.randint(0,ancho_pantalla + 20), random.randint(0,2))
islas.append(isla)
ultimaisla = pygame.time.get_ticks()
proximaisla = random.uniform(2000, 5000) + pygame.time.get_ticks()

clock = pygame.time.Clock()
t_enemigo = pygame.time.get_ticks()
fondo = pygame.sprite.Sprite()

dibuja_fondo()
jugador = Jugador(manual)
pause = False
mov = NADA
salir = False

while vidas >= 0:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
						exit()
		
		marcador = myfont.render("SCORE: " + str(puntos), 0, (255,255,0))
		if vidas >0 :
			marcavidas = myfont.render("PLANES: " + str(vidas), 0, (255,255,0))
		else:
			marcavidas = myfont.render("PLANES: " + str(vidas), 0, (255,0,0))

		
		pressed = pygame.key.get_pressed()

		if pressed[pygame.K_ESCAPE]: exit()

		if pressed[pygame.K_p]: pause = not pause

		if manual and pressed[pygame.K_SPACE] \
		and (pygame.time.get_ticks() - jugador.ultimodisparo >= jugador.temporizador_disparos): 
			puntos -= 1

		if not pause:
			screen.fill((0,0,0,0))
			sprites.draw(screen)
			sprites.update(pressed)
			screen.blit(marcador, (10, 10))
			screen.blit(marcavidas,(460,10))

			# Hay que actualizar la posición real de los enemigos, ya que update() no la toca
			for e in enemigos:
				e[1][1]+= e[0].velocidad

			# Añadimos una isla si toca
			if pygame.time.get_ticks() - ultimaisla > proximaisla:
				ultimaisla = pygame.time.get_ticks()
				proximaisla = random.uniform(500, 1000) + pygame.time.get_ticks()
				isla = Isla(random.randint(0,ancho_pantalla + 20), random.randint(0,2))
				islas.append(isla)

			# Añadimos un enemigo si toca
			if pygame.time.get_ticks() - t_enemigo > 250:
				e_x = random.randint(5, ancho_pantalla-30)
				e_y = -10
				enemigos.append([Enemigo(e_x,e_y, 30, 30, 3, ROJO),[e_x + ancho_enemigo/2,e_y + alto_enemigo/2], True])
				t_enemigo = pygame.time.get_ticks()


			#Busca colisiones
			colisiones(enemigos, jugador, disparos)

			if not manual:
				
				# Crea el estado actual y lanza la búsqueda en profundidad
				e = Estado(puntos, [jugador.rect.x + jugador.ancho/2, jugador.rect.y + jugador.alto/2], enemigos, jugador.velocidad, mov)
				l = busqueda_profundidad(e,0)

				# max() nos devuelve la lista que contiene el mayor elemento de toda la estructura
				mov = l.index(max(l))
				jugador.control(mov)
 
				# Si tenemos que disparar y hay un enemigo en la trayectoria del disparo, lo marcamos como disparado
				# para ignorarlo posteriormente
				if mov == DISPARAR:
					puntos -= 1
					for i in enemigos:	#Cálculos para ver si en caso de disparar habría colisión
						if i[2]:
							if i[1][0] - i[0].radius <= jugador.rect.x + jugador.radius  <= i[1][0]+i[0].radius:
								if i[1][1] <= 485: 	#Posición desde la que aparecen los disparos
									i[2] = False
									break

			if explotar:
				explosion.blit(screen, posicionexplosion)

			if explosion.state == pyganim.STOPPED:
				explotar = False
				explosion.stop()

			# Gestión de memoria. Eliminamos disparos, islas y enemigos que ya se han salido de pantalla
			for i, e in enumerate(enemigos):
				if e[0].rect.y > alto_pantalla + 20:
					e[0].kill()
					del enemigos[i]
				# if e[1][0] > 570:
				# 	e[2] = False

			for i, d in enumerate(disparos):
				if d.rect.y < -10:
					d.kill()
					del disparos[i]

			for i,isla in enumerate(islas):
				if isla.rect.y > alto_pantalla + 20:
					isla.kill()
					del islas[i]

			# Limitamos los FPS a 60 
			clock.tick(60)

		pygame.display.flip()

myfont = pygame.font.Font("fuente.ttf", 50)
gameover = myfont.render("GAME OVER", 0, (255,0,0))

while not salir:
	screen.blit(gameover,(85,270))
	for event in pygame.event.get():
		salir = event.type == pygame.QUIT

	pressed = pygame.key.get_pressed()

	salir = pressed[pygame.K_ESCAPE]

	clock.tick(60)
	pygame.display.flip()



