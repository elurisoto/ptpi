import clases_ptpi

pygame.init()

screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
done = False
enemigos = []

clock = pygame.time.Clock()
t_enemigo = pygame.time.get_ticks()
jugador = Jugador()


while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]: done = True
        
        screen.fill((0, 0, 0))
        
        jugador.controles(pressed)
        jugador.dibuja()

        if pygame.time.get_ticks() - t_enemigo > 750:
            e_x = random.randint(5, 395)
            e_y = -10
            enemigos.append(Enemigo(e_x,e_y, 10, 10, 3, ROJO))
            t_enemigo = pygame.time.get_ticks()


        for e in enemigos:
            e.movimiento()
            e.dibuja()



        pygame.display.flip()
        clock.tick(60)



