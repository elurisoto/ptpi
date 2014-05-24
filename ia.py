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
		self.hijos = None

	# Genera los tres estados hijos de este
	def expandir(self, profundidad):

		l = list(self.lista_enem)
		n_puntuacion = self.puntuacion

		for i in self.lista_enem:	#Cálculos para ver si en caso de disparar habría colisión
			if i[1][0] - 6 <= self.jugador[0] <= i[1][0]+6:
				l.remove(i)
				n_puntuacion +=1
				break

		self.hijos = 	[Estado(self.puntuacion,[self.jugador[0] - self.v, self.jugador[1]], self.lista_enem, self.v),	# Nos movemos a la izquierda
						Estado(self.puntuacion,[self.jugador[0] + self.v, self.jugador[1]], self.lista_enem, self.v),	# A la derecha
						Estado(n_puntuacion, self.jugador, l, self.v)]		# Disparamos
		

	# Función heurística
	def evaluar(self):
		s = self.puntuacion*10 - len(self.lista_enem)*100
		# Buscaremos minimizar la distancia entre el jugador y el primer enemigo (que va a ser el que más abajo está)
		# Posiblemente de mejor resultado acercarse al elemento de la lista con una y más parecida. Se deja esto para más adelante
		if self.lista_enem:

			# Busca cual es la distancia al enemigo más cercano
			d = [abs(i[1][0] - self.jugador[0]) for i in self.lista_enem if i[2]]
			print d
			if d:
				minimo = d[0]
				for i in d:			
					if i < minimo:
						minimo = i
				s -= minimo*100
			# print "--"
			# print self.lista_enem[0][1]
			# print self.jugador
			for i in self.lista_enem:		# Esto debería evitar que choque, pero no va
				if abs(i[1][0] - self.jugador[0]) < 150 and abs(i[1][1] - self.jugador[1]) < 150:
					s = -100000
					print "CUIDADO"

		return s


LIMITE_PROFUNDIDAD = 4

# Aplica una búsqueda en profundidad sobre el arbol de soluciones y devuelve los 
# mejores resultados que se pueden obtener a raíz de cada una de las acciones.
def busqueda_profundidad(e, profundidad):
	
	if profundidad == LIMITE_PROFUNDIDAD:
		return e.evaluar()
	else:
		e.expandir(profundidad)
		l = [busqueda_profundidad(i,profundidad+1) for i in e.hijos]
		return l










