from clases_ptpi import *
from ssheet import *
from sstripanim import *
from copy import copy

def colision_enemigos(enemigos, jugador):
	for i, enem in enumerate (enemigos):
		if pygame.sprite.collide_circle(enemigos[i], jugador):
			enemigos[i].kill()
			del enemigos[i]

def dibuja_fondo():

	fondo.image = ss.image_at((268,367,32,32))
	# fondo.rect = pygame.Rect((0,0,32,32))
	fondo.layer = 2
	# sprites.add(copy(fondo))

	for i in range(0,ancho_pantalla,32):
		for j in range(0,alto_pantalla,32):

			fondo.rect = pygame.Rect((i,j,32,32))
			sprites.add(copy(fondo)) 		#No me convence



pygame.init()

done = False
enemigos = []

clock = pygame.time.Clock()
t_enemigo = pygame.time.get_ticks()
fondo = pygame.sprite.Sprite()

dibuja_fondo()

jugador = Jugador()


while not done:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
						done = True
		
		pressed = pygame.key.get_pressed()

		if pressed[pygame.K_ESCAPE]: done = True
		
		#screen.fill((0, 67, 171))
		screen.fill((0,0,0,0))
		jugador.update(pressed)
		sprites.draw(screen)

		if pygame.time.get_ticks() - t_enemigo > 750:
			e_x = random.randint(5, 370)
			e_y = -10
			enemigos.append(Enemigo(e_x,e_y, 30, 30, 3, ROJO))
			t_enemigo = pygame.time.get_ticks()


		colision_enemigos(enemigos, jugador)

		for i, e in enumerate(enemigos):
			e.update()

			if e.rect.y > 620:
				e.kill()
				del enemigos[i]


		for i, d in enumerate(disparos):
			d.update()

			if d.rect.y < -10:
				d.kill()
				del disparos[i]



		pygame.display.flip()
		clock.tick(60)



