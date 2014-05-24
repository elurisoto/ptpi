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
		if pygame.sprite.collide_circle(enem[0], jugador):	# Busca colisiones enemigo-jugador
			explotar = True
			posicionexplosion = (enem[0].rect.x, enem[0].rect.y)
			explosion.play()
			enem[0].kill()
			enemigos.remove(enem)
			

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
				puntos += 1
				marcador = myfont.render("SCORE: " + str(puntos), 0, (255,255,0))
					


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

myfont = pygame.font.Font("fuente.ttf", 15)
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
			screen.fill((0,0,0,0))
			sprites.draw(screen)
			sprites.update(pressed)
			screen.blit(marcador, (10, 10))

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
			if pygame.time.get_ticks() - t_enemigo > 500:
				e_x = random.randint(5, ancho_pantalla-30)
				e_y = -10
				enemigos.append([Enemigo(e_x,e_y, 30, 30, 3, ROJO),[e_x + ancho_enemigo/2,e_y + alto_enemigo/2], True])
				t_enemigo = pygame.time.get_ticks()


			#Busca colisiones
			colisiones(enemigos, jugador, disparos)

			# Crea el estado actual y lanza la búsqueda en profundidad
			e = Estado(puntos, [jugador.rect.x + jugador.ancho/2, jugador.rect.y + jugador.alto/2], enemigos, jugador.velocidad)
			l = busqueda_profundidad(e,0)

			# max() nos devuelve la lista que contiene el mayor elemento de toda la estructura
			mov = l.index(max(l))
			jugador.control(mov)

			# Si tenemos que disparar y hay un enemigo en la trayectoria del disparo, lo marcamos como disparado
			# para ignorarlo posteriormente
			if mov == DISPARAR:
				for i in enemigos:	#Cálculos para ver si en caso de disparar habría colisión
					if i[2]:
						if i[1][0] - ancho_enemigo/2 <= jugador.rect.x + jugador.ancho/2  <= i[1][0]+ancho_enemigo/2:
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



