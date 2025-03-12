'''Calcula la distancia de Levenshtein entre dos palabras'''
import Levenshtein

# Distancia entre dos palabras
print(Levenshtein.distance("gato", "pato"))  # Salida: 1
print(Levenshtein.distance("silla", "salón"))  # Salida: 3
print(Levenshtein.distance("casa", "caso"))  # Salida: 1
