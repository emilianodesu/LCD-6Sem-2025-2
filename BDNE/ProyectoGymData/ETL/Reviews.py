import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json
import argparse
import logging

load_dotenv()

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_random_reviews(n: int) -> list[dict]:
    """
    Obtiene una muestra aleatoria de reseñas a partir de tres colecciones de MongoDB:
        - citas_programacion
        - citas_game_of_thrones
        - citas_estoicas
    La función realiza las siguientes etapas:
        1. Conexión a MongoDB usando la variable de entorno MONGO_URI.
        2. Carga de cada colección en un DataFrame de pandas.
        3. Eliminación de la columna '_id' y transformación (renombrar y eliminar columnas innecesarias).
        4. Concatenación de todos los DataFrames en uno solo.
        5. Muestreo aleatorio de hasta `n` registros.
        6. Conversión de la muestra a una lista de diccionarios.
    Parámetros:
            n (int): Número máximo de reseñas a retornar.
    Retorna:
            list[dict]: Lista de diccionarios con clave 'comment' y el texto de cada reseña.
    """
    logging.info(f"Iniciando ETL de reseñas: solicitando {n} registros.")

    # Establecer conexión a MongoDB
    mongo_uri = os.getenv("MONGO_URI")
    logging.info(f"Conectando a MongoDB en {mongo_uri}")
    client = MongoClient(mongo_uri)
    db = client.get_default_database()
    logging.info("Conexión a MongoDB establecida.")

    # Cargar colecciones en DataFrames
    citas_programacion = pd.DataFrame(list(db['citas_programacion'].find()))
    logging.info(f"Cargada colección 'citas_programacion' ({len(citas_programacion)} registros).")
    citas_game_of_thrones = pd.DataFrame(list(db['citas_game_of_thrones'].find()))
    logging.info(f"Cargada colección 'citas_game_of_thrones' ({len(citas_game_of_thrones)} registros).")
    citas_estoicas = pd.DataFrame(list(db['citas_estoicas'].find()))
    logging.info(f"Cargada colección 'citas_estoicas' ({len(citas_estoicas)} registros).")

    # Eliminar columna '_id' si existe
    for name, df in [
        ("citas_programacion", citas_programacion),
        ("citas_game_of_thrones", citas_game_of_thrones),
        ("citas_estoicas", citas_estoicas)
    ]:
        if '_id' in df.columns:
            df.drop('_id', axis=1, inplace=True)
            logging.info(f"Columna '_id' eliminada de '{name}'.")

    # Transformaciones específicas por colección
    # citas_programacion
    citas_programacion.rename(columns={'text': 'comment'}, inplace=True)
    citas_programacion.drop(['author', 'numberOfVotes', 'rating', 'source'], axis=1, inplace=True)
    logging.info("Transformaciones aplicadas en 'citas_programacion' (rename & drop).")

    # citas_game_of_thrones
    citas_game_of_thrones.rename(columns={'sentence': 'comment'}, inplace=True)
    citas_game_of_thrones.drop(['character'], axis=1, inplace=True)
    logging.info("Transformaciones aplicadas en 'citas_game_of_thrones' (rename & drop).")

    # citas_estoicas
    citas_estoicas.rename(columns={'quote': 'comment'}, inplace=True)
    citas_estoicas.drop(['author'], axis=1, inplace=True)
    logging.info("Transformaciones aplicadas en 'citas_estoicas' (rename & drop).")

    # Concatenar todos los DataFrames
    df_completo = pd.concat(
        [citas_programacion, citas_game_of_thrones, citas_estoicas],
        axis=0,
        ignore_index=True
    )
    total = len(df_completo)
    logging.info(f"DataFrames concatenados. Total registros disponibles: {total}.")

    # Muestreo aleatorio
    n_sample = min(n, total)
    muestra = df_completo.sample(n=n_sample)
    logging.info(f"Obtenida muestra aleatoria de {n_sample} registros.")

    # Convertir a lista de dicts
    muestra_lista_dict = muestra.to_dict(orient='records')
    logging.info("Conversión de muestra a lista de diccionarios completada.")

    return muestra_lista_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Obtener una muestra aleatoria de reseñas desde MongoDB."
    )
    parser.add_argument(
        '-n', '--num',
        type=int,
        default=10,
        help="Número de reseñas a extraer (por defecto: 10)."
    )
    parser.add_argument(
        '-p', '--path',
        type=str,
        default="reviews.json",
        help="Ruta de salida para el archivo JSON (por defecto: reviews.json)."
    )
    args = parser.parse_args()

    logging.info("Ejecutando proceso ETL de reseñas.")
    muestras = get_random_reviews(args.num)

    logging.info(f"Guardando {len(muestras)} reseñas en '{args.path}'.")
    with open(args.path, "w", encoding="utf-8") as f:
        json.dump(muestras, f, ensure_ascii=False, indent=4)
    logging.info(f"Archivo '{args.path}' guardado correctamente.")
