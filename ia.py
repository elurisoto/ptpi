#-*-coding:utf-8-*-
import math
from clases_ptpi import *

class Estado:

	# lista_enem es una lista como la de enemigos del bucle principal
	# jugador es la componente x de la posición del jugador
	# puntuacion es la puntuación actual
	# v es la velocidad a la que se desplaza el jugador
	def __init__(self, puntuacion, jugador, lista_enem, v):
		self.puntuacion = puntuacion
		self.jugador = jugador
		self.lista_enem = lista_enem
		self.v = v
		self.hijos = None

	# Genera los tres estados hijos de este
	def expandir(self, profundidad):

		l = list(self.lista_enem)
		n_puntuacion = self.puntuacion

		for i in self.lista_enem:	#Cálculos para ver si en caso de disparar habría colisión
			if i[1][0] - 7<= self.jugador[0] <= i[1][0]+7:
				l.remove(i)
				n_puntuacion +=1
				break

		self.hijos = 	[Estado(self.puntuacion,[self.jugador[0] - self.v, self.jugador[1]], self.lista_enem, self.v),	# Nos movemos a la izquierda
						Estado(self.puntuacion,[self.jugador[0] + self.v, self.jugador[1]], self.lista_enem, self.v),	# A la derecha
						Estado(n_puntuacion, self.jugador, l, self.v)]		# Disparamos
		

	# Función heurística
	def evaluar(self):
		s = self.puntuacion*10 + 1000/(len(self.lista_enem)+0.00001)
		# Buscaremos minimizar la distancia entre el jugador y el enemigo más cercano
		if self.lista_enem:
			# Busca cual es la distancia al enemigo más cercano
			d = [abs(i[1][0] - self.jugador[0]) for i in self.lista_enem if i[2]]
			if d:
				minimo = d[0]
				for i in d:			
					if i < minimo:
						minimo = i
				s -= minimo*100

			# Si hay un enemigo demasiado cerca, buscamos evitarlo a toda costa
			for i in self.lista_enem:		
				if i[2]:
					dist = distancia(i[1],self.jugador)
					if dist < 130:
						s -= dist*1000000
						
		return s

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










