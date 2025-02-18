""" Sección 2 """

import random

randoms = [random.randint(0, 15) for _ in range(20)]
print('Lista de números aleatorios:')
print(randoms, end='\n\n')

# 1)
print('[m:n]')
print(randoms[2:12])  # [m:n]
print(randoms[-18:-8], end='\n\n')

# 2)
print('[-m:n]')
print(randoms[-17:13])  # [-m:n]
print(randoms[3:13], end='\n\n')

# 3)
print('[m:]')
print(randoms[5:])  # [m:]
print(randoms[-15:], end='\n\n')

# 4)
print('[:n]')
print(randoms[:7])  # [:n]
print(randoms[:-13], end='\n\n')
