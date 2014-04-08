from clases_ptpi import *
from ssheet import *
from sstripanim import *
from copy import copy

def colisiones(enemigos, jugador, disparos):
	i = j = 0
	for enem in enemigos:
		if pygame.sprite.collide_circle(enem, jugador):
			enem.kill()
			enemigos.remove(enem)

		for disp in disparos:
			if pygame.sprite.collide_circle(disp, enem):
				enem.kill()
				disp.kill()
				enemigos.remove(enem)
				disparos.remove(disp)


def dibuja_fondo():

	fondo.image = ss.image_at((268,367,32,32))
	fondo.layer = 2

	for i in range(0,ancho_pantalla,32):
		for j in range(0,alto_pantalla,32):

			fondo.rect = pygame.Rect((i,j,32,32))
			sprites.add(copy(fondo)) 		#No me convence



pygame.init()

done = False
enemigos = []
islas = []

ultimaisla = 0

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
		# jugador.update(pressed)
		sprites.draw(screen)
		sprites.update(pressed)


		if pygame.time.get_ticks() - ultimaisla > random.gauss(10000, 2000):
			ultimaisla = pygame.time.get_ticks()
			isla = Isla(random.randint(0,ancho_pantalla + 20), random.randint(0,2))
			islas.append(isla)

		if pygame.time.get_ticks() - t_enemigo > 750:
			e_x = random.randint(5, 370)
			e_y = -10
			enemigos.append(Enemigo(e_x,e_y, 30, 30, 3, ROJO))
			t_enemigo = pygame.time.get_ticks()



		colisiones(enemigos, jugador, disparos)



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

		pygame.display.flip()
		clock.tick(60)



