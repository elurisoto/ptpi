#-*-coding:utf-8-*-

from clases_ptpi import *

class Estado:

	# lista_enem es una lista con las posiciones (en principio en el eje x) de los enemigos
	# jugador es la componente x de la posición del jugador
	# puntuacion es la puntuación actual
	# v es la velocidad a la que se desplaza el jugador
	def __init__(self, puntuacion, jugador, lista_enem, v):
		self.puntuacion = puntuacion
		self.jugador = jugador
		self.lista_enem = lista_enem
		self.v = v

	# Genera los tres estados hijos de este
	def hijos(self):
		h = []

		# Nos movemos a la izquierda
		h.append(Estado(self.puntuacion,self.jugador - self.v, self.lista_enem, self.v))
		# Nos movemos a la derecha
		h.append(Estado(self.puntuacion,self.jugador + self.v, self.lista_enem, self.v))

		l = list(self.lista_enem)
		n_puntuacion = self.puntuacion
		# Disparamos
		for i in self.lista_enem:
			if i - 6 <= self.jugador <= i+6:
				l.remove(i)
				n_puntuacion +=1
				break

		h.append(Estado(n_puntuacion, self.jugador, l, self.v))

		return h

	# Función heurística
	def evaluar(self):
		s = self.puntuacion*100 - len(self.lista_enem)*100
		# Buscaremos minimizar la distancia entre el jugador y el primer enemigo (que va a ser el que más abajo está)
		# Posiblemente de mejor resultado acercarse al elemento de la lista con una y más parecida. Se deja esto para más adelante
		if self.lista_enem:

			d = [abs(i - self.jugador) for i in self.lista_enem]
			minimo = d[0]
			for i in d:
				if i < minimo:
					minimo = i
			s -= minimo

			#d = abs(self.lista_enem[i] - self.jugador)


		return s











	