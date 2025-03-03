"""Programa para contar las palabras de manera secuencial"""
import time
import string

def count_words(value):
    """Cuenta las palabras de un texto"""
    word_count = {}
    for line in value:
        line = line.translate(str.maketrans('', '', string.punctuation)).lower()
        words = line.split()
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
    return word_count


if __name__ == '__main__':
    with open('big.txt', 'r', encoding='utf-8') as file:
        text = file.readlines()

    start_time = time.time()
    result = count_words(text)
    end_time = time.time()

    sorted_result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    print(dict(list(sorted_result.items())[:50]))
    print(f"Tiempo de ejecución: {end_time - start_time:.4f} segundos")
