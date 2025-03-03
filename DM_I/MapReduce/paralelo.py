"""Version map reduce con un txt grande"""
import string
from multiprocessing import Pool
import time


def map_function(value):
    """Divide el texto en palabras y asigna un valor de 1 a cada palabra"""
    value = value.translate(str.maketrans('', '', string.punctuation)).lower()
    words = value.split()
    return [(word, 1) for word in words]

def reduce_function(pairs):
    """Agrupa las palabras y suma sus ocurrencias"""
    word_count = {}
    for word, count in pairs:
        word_count[word] = word_count.get(word, 0) + count
    return word_count


if __name__ == '__main__':
    with open('big.txt', 'r', encoding='utf-8') as file:
        text = file.readlines()

    start_time = time.time()
    with Pool() as pool:
        mapped_values = pool.map(map_function, text)
    flattened_pairs = [pair for sublist in mapped_values for pair in sublist]
    result = reduce_function(flattened_pairs)
    end_time = time.time()


    sorted_result = dict(
        sorted(result.items(), key=lambda item: item[1], reverse=True))
    print(dict(list(sorted_result.items())[:50]))
    print(f"Tiempo de ejecución: {end_time - start_time:.4f} segundos")
