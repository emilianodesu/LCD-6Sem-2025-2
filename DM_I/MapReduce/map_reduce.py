from multiprocessing import Pool
# text = ['hola mundo','hola de nuevo','mundo de datos']

# Funcion Map: Divide el texto en palabras y asigna un valor de 1 a cada palabra
def map_function(value):
    words = value.split()
    return [(word, 1) for word in words]

# Funcion Reduce: Agrupa las palabras y suma sus ocurrencias

def reduce_function(pairs):
    word_count = {}
    for word, count in pairs:
        word_count[word] = word_count.get(word, 0) + count
    return word_count

# Simulacion del proceso
if __name__ == '__main__':
    text = ['hola mundo','hola de nuevo','mundo de datos']

    # Fase Map (procesamiento en paralelo)
    with Pool() as pool:
        mapped_values = pool.map(map_function, text)

    # Aplanar la lista de pares clave-valor
    flattened_pairs = [pair for sublist in mapped_values for pair in sublist]

    # Fase Reduce (agregacion)
    result = reduce_function(flattened_pairs)
    print(result)