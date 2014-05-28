#-*-coding:utf-8-*-
import math
from clases_ptpi import *

class Estado:

	# lista_enem es una lista como la de enemigos del bucle principal
	# jugador es la componente x de la posición del jugador
	# puntuacion es la puntuación actual
	# v es la velocidad a la que se desplaza el jugador
	def __init__(self, puntuacion, jugador, lista_enem, v, accion):
		self.puntuacion = puntuacion
		self.jugador = jugador
		self.lista_enem = lista_enem
		self.v = v
		self.hijos = None
		self.accion = accion
		self.colision = False

	# Genera los tres estados hijos de este
	def expandir(self, profundidad):

		l = list(self.lista_enem)
		n_puntuacion = self.puntuacion

		for i in self.lista_enem:	#Cálculos para ver si en caso de disparar habría colisión
			if i[2]:
				if i[1][0] - ancho_enemigo/2 +3 <= self.jugador[0] <= i[1][0]+ancho_enemigo/2-3:
					l.remove(i)
					n_puntuacion +=10
					self.colision = True
					break


		self.hijos = 	[Estado(self.puntuacion,[self.jugador[0] - self.v, self.jugador[1]], self.lista_enem, self.v, IZQUIERDA),	# Nos movemos a la izquierda
						Estado(self.puntuacion,[self.jugador[0] + self.v, self.jugador[1]], self.lista_enem, self.v, DERECHA),	# A la derecha
						Estado(n_puntuacion-1, self.jugador, l, self.v, DISPARAR),		# Disparamos
						Estado(self.puntuacion, self.jugador, self.lista_enem, self.v, NADA)]		# No hacemos nada
		

	# Función heurística
	def evaluar(self):
		s = self.puntuacion*100000 + 100000/(len(self.lista_enem)+0.00001)
		# if not(self.colision) and self.accion == DISPARAR:
		# 	s=-100000
		#print "[" + str(self.accion) + "]" + str(s)

		# Buscaremos minimizar la distancia entre el jugador y el enemigo más cercano
		if self.lista_enem:
			# Busca cual es la distancia al enemigo más cercano
			#d = [10.0/(abs(i[1][0] - self.jugador[0])+0.000001) for i in self.lista_enem if i[2]]
			d = [abs(i[1][0] - self.jugador[0]) for i in self.lista_enem if i[2]]

			if d:
				# minimo = d[0]
				# for i in d:			
				# 	if i < minimo:
				# 		minimo = i
				s -= min(d)*100
			#s+=sum(d)

			# Si hay un enemigo demasiado cerca, buscamos evitarlo a toda costa
			for i in self.lista_enem:		
				if i[2]:
					dist = distancia(i[1],self.jugador)
					if dist <= 75:
						s += dist*1000
					# if enRectangulo(i[1], self.jugador):
					# 	dist = distancia(i[1],self.jugador)
					# 	s += dist*1000
						
		return s

# Comprueba si el enemigo está dentro de un rectángulo que rodea al jugador
def enRectangulo(enemigo, jugador):
	# Calculamos los límites del rectángulo
	xmin = jugador[0] - 40
	xmax = jugador[0] + 75
	ymin = jugador[1] - 75
	ymax = jugador[1] + 75

	if enemigo[0] > xmin and enemigo[0] < xmax and enemigo[1] > ymin and enemigo[1] < ymax:
		return True

	return False


#Calcula la distancia euclídea entre dos puntos
def distancia(a,b):
	x = a[0] - b[0]
	y = a[1] - b[1]
	return math.sqrt(x*x + y*y)

LIMITE_PROFUNDIDAD = 4

# Genera el arbol de soluciones. La mejor de ella se busca con max()
def busqueda_profundidad(e, profundidad):
	
	if profundidad == LIMITE_PROFUNDIDAD:
		return e.evaluar()
	else:
		e.expandir(profundidad)
		l = [busqueda_profundidad(i,profundidad+1) for i in e.hijos]
		return l










