from Gyms import get_random_gyms
from Reviews import get_random_reviews
from Users import get_random_users
from dotenv import load_dotenv
import os
from pymongo import MongoClient,UpdateOne
from datetime import datetime
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import logging
from bson import ObjectId
from collections import Counter
import time
import argparse
import re
# configuracion de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def mapCanonicalUserToMongoDB(user,favoritos = []):
    """
    Mapea un objeto de usuario canónico a la estructura adecuada para persistir en MongoDB.

    Args:
        user (dict): Diccionario que contiene los datos del usuario con las claves:
            - "nombre" (str)
            - "email" (str)
            - "role" (str)
            - "createdAt" (str, formato "%Y-%m-%d %H:%M:%S")
            - "updatedAt" (str, formato "%Y-%m-%d %H:%M:%S")
            - "direccion" (dict) con:
                - "calle" (str)
                - "estado" (str)
                - "municipio" (str)
                - "longitude" (str o numérico)
                - "latitude" (str o numérico)
        favoritos (list, opcional): Lista de elementos favoritos a asociar al usuario. Por defecto, [].

    Returns:
        dict: Representación del usuario para MongoDB, con:
            - "nombre" (str)
            - "email" (str) libre de caracteres nulos
            - "favoritos" (list)
            - "role" (str)
            - "createdAt" (datetime)
            - "updatedAt" (datetime)
            - "direccion" (dict) que incluye:
                - "calle" (str)
                - "estado" (str)
                - "municipio" (str)
                - "ubicacion" (GeoJSON Point con [longitud, latitud])
    """
    raw_email = str(user["email"])
    clean_email = raw_email.replace("\x00", "")
    return {
        "nombre": str(user["nombre"]),
        "email": clean_email,
        "favoritos" : [f for f in favoritos],
        "role": str(user["role"]),
        "createdAt" : datetime.strptime(user["createdAt"], "%Y-%m-%d %H:%M:%S"),
        "updatedAt" : datetime.strptime(user["updatedAt"], "%Y-%m-%d %H:%M:%S"),
        "direccion" : {
            "calle" : str(user["direccion"]["calle"]),
            "estado" : str(user["direccion"]["estado"]),
            "municipio" : str(user["direccion"]["municipio"]),
            "ubicacion" : {
                "type" : "Point",
                "coordinates" : [
                    float(user["direccion"]["longitude"]),
                    float(user["direccion"]["latitude"])
                ]
            }
        }
    }

def mapCanonicalGymToMongoDB(gym,owner_id = None):
    """
    Convierte un diccionario con esquema canónico de gimnasio en un documento listo para almacenar en MongoDB.

    Args:
        gym (dict): Diccionario que contiene los datos del gimnasio. Debe incluir:
            - "nombre" (str|Any): Nombre del gimnasio.
            - "direccion" (str|Any): Dirección física.
            - "ubicacion" (Iterable[float]): Coordenadas [longitud, latitud].
            - "precio" (float|Any): Precio de suscripción o acceso.
            - "actividades" (Iterable): Lista de actividades que ofrece.
            - "servicios" (Iterable): Lista de servicios disponibles.
            - "averageRating" (float|Any): Valoración media existente.
            - "createdAt" (str): Fecha de creación en formato "%Y-%m-%d %H:%M:%S".
            - "updatedAt" (str): Fecha de última actualización en formato "%Y-%m-%d %H:%M:%S".
        owner_id (str|ObjectId, opcional): Identificador del propietario; si no se provee, se asigna None.

    Returns:
        dict: Documento con la siguiente estructura para MongoDB:
            - nombre (str)
            - direccion (str)
            - ubicacion (dict): GeoJSON con "type": "Point" y "coordinates": [longitud, latitud]
            - precio (float)
            - actividades (list)
            - servicios (list)
            - ownerId (ObjectId | None)
            - averageRating (float)
            - reviewCount (int) inicializado a 0
            - createdAt (datetime)
            - updatedAt (datetime)
            - followers (list) inicializado vacío

    Raises:
        KeyError: Si falta alguna de las claves obligatorias en el diccionario `gym`.
        ValueError: Si falla la conversión de tipos o el parseo de fechas.
    """
    return {
        "nombre" : str(gym["nombre"]),
        "direccion" : str(gym["direccion"]),
        "ubicacion" : {
            "type" : "Point",
            "coordinates" : list(gym["ubicacion"])
        },
        "precio" : float(gym["precio"]),
        "actividades" : list(gym["actividades"]),
        "servicios" : list(gym["servicios"]),
        "ownerId" : ObjectId(str(owner_id)) if owner_id else None,
        "averageRating" : float(gym["averageRating"]),
        "reviewCount" : 0,
        "createdAt" : datetime.strptime(gym["createdAt"], "%Y-%m-%d %H:%M:%S"),
        "updatedAt" : datetime.strptime(gym["updatedAt"], "%Y-%m-%d %H:%M:%S"),
        "followers" : [],
    }



def main(params):
    """
    Función principal que genera y sube datos de gimnasios, usuarios y reseñas a MongoDB.
    Parámetros:
        params (dict): Diccionario con parámetros opcionales:
            - num_gyms (int): número de gimnasios a generar (por defecto 100).
            - num_reviews (int): número de reseñas a generar (por defecto 100).
            - num_users (int): número de usuarios a generar (por defecto 4).
    Acciones:
        1. Lee la URI de MongoDB desde la variable de entorno 'MONGO_URI_BULK'.
        2. Genera concurrentemente gimnasios, reseñas y usuarios aleatorios.
        3. Inserta usuarios normales y propietarios en la colección 'users'.
        4. Inserta gimnasios en la colección 'gyms'.
        5. Asigna propietarios a gimnasios de forma aleatoria mediante bulk_write.
        6. Inserta reseñas en la colección 'reviews'.
        7. Actualiza en bulk el contador de reseñas ('reviewCount') en cada gimnasio.
        8. Genera listas de favoritos de usuarios a gimnasios y actualiza en bulk
           las colecciones 'users' (campo 'favoritos') y 'gyms' (campo 'followers').
    Retorna:
        None
    """
    uri_mongo_bulk = os.getenv("MONGO_URI_BULK")
    num_gyms = params.get("num_gyms", 100)
    num_reviews = params.get("num_reviews", 100)
    num_users = params.get("num_users", 4)
    logging.info(f"Generando {num_gyms} gimnasios, {num_reviews} reviews y {num_users} usuarios.")
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_gyms    = executor.submit(get_random_gyms,    num_gyms)
        future_reviews = executor.submit(get_random_reviews, num_reviews)
        future_users   = executor.submit(get_random_users,   num_users)

        gyms    = future_gyms.result()
        review  = future_reviews.result()
        users   = future_users.result()
    logging.info(f"Generación de datos completada: {len(gyms)} gimnasios, {len(review)} reviews y {len(users)} usuarios.")
    owner_users = list(filter(lambda x: x["role"] == "owner", users))
    normal_users = list(filter(lambda x: x["role"] == "user", users))
    # crear usuarios de mongoDB
    normal_users_mongo = list(map(lambda x: mapCanonicalUserToMongoDB(x), normal_users))
    # upload owners users
    client = MongoClient(uri_mongo_bulk)
    db = client.get_default_database()

    # Insertar usuarios normales
    normal_users_result_ids = db.users.insert_many(normal_users_mongo).inserted_ids
    logging.info(f"Usuarios normales subidos a MongoDB: {len(normal_users_result_ids)}")

    # Insertar usuarios owners
    owner_users_mongo = [mapCanonicalUserToMongoDB(u) for u in owner_users]
    owner_users_result_ids = db.users.insert_many(owner_users_mongo).inserted_ids
    logging.info(f"Usuarios owners subidos a MongoDB: {len(owner_users_result_ids)}")

    # Insertar gimnasios
    gyms_mongo = [mapCanonicalGymToMongoDB(g) for g in gyms]
    gyms_mongo_ids = db.gyms.insert_many(gyms_mongo).inserted_ids
    logging.info(f"Gimnasios subidos a MongoDB: {len(gyms_mongo_ids)}")

    # Asignar ownerId a un subset aleatorio de gimnasios usando bulk_write
    count = min(len(owner_users_result_ids), len(gyms_mongo_ids))
    chosen_gyms = list(np.random.choice(gyms_mongo_ids, size=count, replace=False))
    updates = [
        UpdateOne({'_id': gym_id}, {'$set': {'ownerId': owner_id}})
        for gym_id, owner_id in zip(chosen_gyms, owner_users_result_ids)
    ]
    if updates:
        result = db.gyms.bulk_write(updates)
        logging.info(f"Gimnasios actualizados con owner: {result.modified_count}")
    all_ids_users = normal_users_result_ids + owner_users_result_ids

    # generar pares de user_id y gym_id para los reviews
    user_ids_for_reviews = np.random.choice(all_ids_users, size=num_reviews, replace=True)
    gym_ids_for_reviews = np.random.choice(gyms_mongo_ids, size=num_reviews, replace=True)
    review_pairs = list(zip(user_ids_for_reviews, gym_ids_for_reviews))

    # preparar reviews para insertar y calcular reviewCount localmente
    reviews = []
    for i, (user_id, gym_id) in enumerate(review_pairs):
        reviews.append({
            "userId":    ObjectId(str(user_id)),
            "gymId":     ObjectId(str(gym_id)),
            "rating" :int(np.random.randint(1, 6)),
            "comentario":   str(review[i]["comment"]) if i < len(review) else "Comentario de prueba",
            "createdAt": datetime.now()
        })

    # insertar los reviews en MongoDB
    db.reviews.insert_many(reviews)

    # calcular counts por gymId
    gym_review_counts = Counter(r["gymId"] for r in reviews)

    # bulk update de reviewCount en gyms
    updates = [
        UpdateOne({"_id": gym_id}, {"$set": {"reviewCount": int(count)}})
        for gym_id, count in gym_review_counts.items()
    ]
    if updates:
        result = db.gyms.bulk_write(updates)
        logging.info(f"Gimnasios actualizados con reviewCount: {result.modified_count}")

    # favoritos entre usuarios y gyms (optimizado con bulk_write)
    max_favs = min(9, len(gyms_mongo_ids))
    # generar número de favoritos por usuario
    num_favoritos_por_usuario = np.random.randint(0, max_favs, size=len(all_ids_users))
    user_updates = []
    gym_followers = {}
    for user_id, n_fav in zip(all_ids_users, num_favoritos_por_usuario):
        if n_fav <= 0:
            continue
        favs = np.random.choice(gyms_mongo_ids, size=n_fav, replace=False).tolist()
        user_updates.append(
            UpdateOne({'_id': ObjectId(str(user_id))}, {'$set': {'favoritos': [
                ObjectId(str(gym_id)) for gym_id in favs
            ]}})
        )
        for gym_id in favs:
            gym_followers.setdefault(gym_id, []).append(user_id)
    # bulk update usuarios
    if user_updates:
        result = db.users.bulk_write(user_updates)
        logging.info(f"Usuarios actualizados con favoritos: {result.modified_count}")
    # bulk update gimnasios
    gym_updates = [
        UpdateOne({'_id': ObjectId(str(gym_id))}, {'$addToSet': {'followers': {'$each': [ObjectId(str(uid)) for uid in uids]}}})
        for gym_id, uids in gym_followers.items()
    ]
    if gym_updates:
        result = db.gyms.bulk_write(gym_updates)
        logging.info(f"Gimnasios actualizados con followers: {result.modified_count}")

def parse_args():
    """
    Parsea los argumentos de la línea de comandos para la inserción por lotes
    de datos de gimnasios, usuarios y reseñas en MongoDB.

    Returns:
        argparse.Namespace: Objeto con los siguientes atributos:
            iterations (int): Número de veces que se ejecuta la función main (por defecto 1).
            num_gyms (int): Cantidad de gimnasios a generar en cada iteración (por defecto 50).
            num_reviews (int): Cantidad de reseñas a generar en cada iteración (por defecto 200).
            num_users (int): Cantidad de usuarios a generar en cada iteración (por defecto 400).
    """
    parser = argparse.ArgumentParser(
        description="Inserta datos de gimnasios, usuarios y reseñas en MongoDB en lotes."
    )
    parser.add_argument(
        "-n", "--iterations",
        type=int,
        default=1,
        help="Número de veces que se ejecuta la función main"
    )
    parser.add_argument(
        "--num-gyms",
        type=int,
        default=50,
        help="Cantidad de gimnasios a generar en cada iteración"
    )
    parser.add_argument(
        "--num-reviews",
        type=int,
        default=200,
        help="Cantidad de reseñas a generar en cada iteración"
    )
    parser.add_argument(
        "--num-users",
        type=int,
        default=400,
        help="Cantidad de usuarios a generar en cada iteración"
    )
    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()
    args = parse_args()

    uri_bulk = os.getenv("MONGO_URI_BULK")
    # censura la contraseña entre ":" y "@"
    uri_masked = re.sub(r"(mongodb(?:\+srv)?://[^:]+:)[^@]+@", r"\1****@", uri_bulk or "")
    print(f"Conectando a MongoDB en {uri_masked}")
    input("Presione Enter para continuar...")

    for i in range(args.iterations):
        print("\n" * 5)
        logging.info(f"Ejecutando iteración {i+1} de {args.iterations}.")
        try:
            main({
                "num_gyms":    args.num_gyms,
                "num_reviews": args.num_reviews,
                "num_users":   args.num_users,
            })
        except Exception as e:
            logging.error(f"Error en la iteración {i+1}: {e}")
        time.sleep(0.2)