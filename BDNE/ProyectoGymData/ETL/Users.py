import requests
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from geopy.geocoders import Nominatim
import datetime
import json
import random
import time
import os
import logging
from dotenv import load_dotenv
load_dotenv()

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def sample_gaussian_in_polygon(polygon: Point, num_points: int, sigma: float) -> list[tuple[float, float]]:
    """
    Genera una muestra de puntos con distribución gaussiana dentro de un polígono.

    Esta función crea puntos aleatorios siguiendo una distribución normal (gaussiana)
    centrada en el centroide del polígono. Solo se incluyen en la muestra los puntos
    que caen dentro del polígono.

    Args:
        polygon (Point): Polígono que delimita el área donde se generarán los puntos.
        num_points (int): Número de puntos a generar.
        sigma (float): Desviación estándar para la distribución gaussiana.

    Returns:
        list[tuple[float, float]]: Lista de puntos (longitud, latitud) generados dentro del polígono.
    """
    centroid = polygon.centroid
    samples: list[tuple[float, float]] = []
    while len(samples) < num_points:
        lon, lat = np.random.normal(loc=[centroid.x, centroid.y], scale=sigma)
        point = Point(lon, lat)
        if polygon.contains(point):
            samples.append((lon, lat))
    return samples

def get_random_users(count: int) -> list[dict]:
    """
    Genera una lista de usuarios aleatorios con datos demográficos y geográficos para la CDMX, usando Mockaroo y un shapefile de alcaldías.
    Args:
        count (int): Número de usuarios a generar. Debe ser mayor que 1.
    Returns:
        list[dict]: Lista de diccionarios, cada uno con las claves:
            - nombre (str): Nombre completo del usuario.
            - email (str): Correo electrónico.
            - role (str): 'user' o 'owner'.
            - direccion (dict): Datos de ubicación con las claves:
                * estado (str)
                * municipio (str)
                * latitude (float)
                * longitude (float)
                * calle (str)
            - createdAt (str): Fecha y hora de creación en formato "YYYY-MM-DD HH:MM:SS".
            - updatedAt (str): Fecha y hora de actualización igual a createdAt.
    Raises:
        ValueError: Si count ≤ 1 o si alguna alcaldía del diccionario de población no se encuentra en el shapefile.
        Exception: Si la API de Mockaroo devuelve un código de error.
    Notes:
        - Se muestrean coordenadas dentro de cada alcaldía aplicando una distribución gaussiana.
        - Aproximadamente el 5% de los usuarios seleccionados (count * 0.05) son geocodificados inversamente con Nominatim.
        - Garantiza al menos un 'user' y un 'owner' en el conjunto final.
    """
    if count <= 1:
        raise ValueError("Number of users must be greater than 1.")

    logging.info(f"Iniciando generación de {count} usuarios.")

    # Determinar qué usuarios van a recibir geocodificación (0.5%)
    num_to_geocode = int(count * 0.05)
    geocode_indices = set(random.sample(range(count), num_to_geocode))
    logging.info(f"Se geocodificarán inversamente {num_to_geocode} usuarios (índices: {sorted(geocode_indices)}).")

    # Cargar shapefile de alcaldías
    boroughs_gdf = gpd.read_file("./alcaldias/poligonos_alcaldias_cdmx.shp")
    logging.info("Shapefile de alcaldías cargado correctamente.")

    # Datos de población por alcaldía (igual que antes)…
    population = {
        "Álvaro Obregón": 759137,
        "Azcapotzalco": 432205,
        "Benito Juárez": 434153,
        "Coyoacán": 614447,
        "Cuajimalpa de Morelos": 217686,
        "Cuauhtémoc": 545884,
        "Gustavo A. Madero": 1173351,
        "Iztacalco": 404695,
        "Iztapalapa": 1835486,
        "La Magdalena Contreras": 247622,
        "Miguel Hidalgo": 414470,
        "Milpa Alta": 152685,
        "Tláhuac": 392313,
        "Tlalpan": 699928,
        "Venustiano Carranza": 443704,
        "Xochimilco": 442178
    }

    # Validar nombres en shapefile
    shapefile_names = boroughs_gdf['NOMGEO'].tolist()
    for name in population:
        if name not in shapefile_names:
            raise ValueError(f"Borough '{name}' not found in shapefile.")
    logging.info("Todas las alcaldías validadas en el shapefile.")

    # Preparar probabilidades y geometrías
    borough_list = list(population.keys())
    weights = [population[name] for name in borough_list]
    probabilities = [w / sum(weights) for w in weights]
    geometry_map = {row['NOMGEO']: row['geometry'] for _, row in boroughs_gdf.iterrows()}

    # Obtener datos de Mockaroo
    logging.info("Solicitando datos a Mockaroo...")
    response = requests.get(
        "https://my.api.mockaroo.com/user_data_random",
        params={'key': os.getenv('MOCKARO_KEY'), 'count': count}
    )
    if response.status_code != 200:
        logging.error(f"Mockaroo API error: {response.status_code} - {response.text}")
        raise Exception(f"Mockaroo API error: {response.status_code} - {response.text}")
    mockaroo_data = response.json()
    logging.info("Datos recibidos de Mockaroo.")

    # Inicializar geocoder
    geolocator = Nominatim(user_agent="user_data_generator")

    usuarios: list[dict] = []
    total_processed = 0
    attempts = 0
    success = 0

    for idx, record in enumerate(mockaroo_data):
        total_processed += 1

        # Datos básicos
        nombre = record['fullName']
        email = record['email']
        ts = datetime.datetime.strptime(
            f"{record['createdAtDate']} {record['createdAtTime']}",
            "%Y-%m-%d %H:%M:%S"
        )
        role = 'user' if random.random() < 0.9 else 'owner'
        borough = np.random.choice(borough_list, p=probabilities)
        lon, lat = sample_gaussian_in_polygon(geometry_map[borough], 1, sigma=0.02)[0]

        # Decidir si geocodificar o no
        if idx in geocode_indices:
            attempts += 1
            street = None
            try:
                location = geolocator.reverse((lat, lon), exactly_one=True, language='es')
                time.sleep(1.1)
                if location:
                    addr = location.raw.get('address', {})
                    street = addr.get('road')
                    if street:
                        success += 1
            except Exception as e:
                logging.warning(f"Error en geocodificación inversa (usuario {idx}): {e}")

            pct = (success / attempts * 100) if attempts else 0
            logging.info(f"Geocodificación inversa: {success}/{attempts} éxitos ({pct:.2f}%).")

        else:
            street = "SIN GEODECODIFICACION"
            logging.debug(f"Usuario {idx}: asignada etiqueta SIN GEODECODIFICACION.")

        # Construir dirección y usuario
        direccion = {
            "estado": "Ciudad de México",
            "municipio": borough,
            "latitude": float(lat),
            "longitude": float(lon),
            "calle": street or "Calle no encontrada"
        }
        usuarios.append({
            "nombre": nombre,
            "email": email,
            "role": role,
            "direccion": direccion,
            "createdAt": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "updatedAt": ts.strftime("%Y-%m-%d %H:%M:%S")
        })

    # Asegurar al menos un owner y un user
    owners_count = sum(1 for u in usuarios if u['role'] == 'owner')
    users_count = sum(1 for u in usuarios if u['role'] == 'user')
    if owners_count == 0:
        usuarios[-1]['role'] = 'owner'
    if users_count == 0:
        usuarios[-1]['role'] = 'user'

    logging.info(f"Generación completada: {len(usuarios)} usuarios creados.")
    return usuarios

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate random users.")
    parser.add_argument(
        '-n', '--num',
        type=int,
        default=10,
        help="Number of users to generate (default: 10)."
    )
    parser.add_argument(
        '-p', '--path',
        type=str,
        default="users.json",
        help="Output file path for JSON data (default: users.json)."
    )
    args = parser.parse_args()

    users = get_random_users(args.num)

    with open(args.path, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
    logging.info(f"Archivo '{args.path}' guardado con {len(users)} registros.")
