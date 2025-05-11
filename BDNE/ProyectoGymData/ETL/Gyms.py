import os
import json
import logging
import argparse
from datetime import date, timedelta
from dotenv import load_dotenv
from pydantic import BaseModel, validate_call
from scipy.stats import gamma
import concurrent.futures
import numpy as np
import requests
load_dotenv()

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class BuscarAreaActParams(BaseModel):
    """
    Parámetros para consultar el endpoint BuscarAreaAct de INEGI.
    """
    entidadFederativa: str = "00"
    municipio: str = "0"
    localidad: str = "0"
    ageb: str = "0"
    manzana: str = "0"
    sector: str = "0"
    subsector: str = "0"
    rama: str = "0"
    clase: str = "0"
    nombre: str = "0"
    id: str = "0"
    registroInicial: int = 1
    registroFinal: int = 100
    token: str

    def url(self) -> str:
        partes = [
            self.entidadFederativa, self.municipio, self.localidad,
            self.ageb, self.manzana, self.sector, self.subsector,
            self.rama, self.clase, self.nombre,
            str(self.registroInicial), str(self.registroFinal),
            self.id, self.token,
        ]
        url = f"https://www.inegi.org.mx/app/api/denue/v1/consulta/BuscarAreaAct/{'/'.join(partes)}"
        logging.debug(f"URL construida: {url}")
        return url

@validate_call()
def build_buscar_area_act_url(
    token: str,
    entidadFederativa: str = "00",
    municipio: str = "0",
    localidad: str = "0",
    ageb: str = "0",
    manzana: str = "0",
    sector: str = "0",
    subsector: str = "0",
    rama: str = "0",
    clase: str = "0",
    nombre: str = "0",
    id: str = "0",
    registroInicial: int = 1,
    offset: int = 0,
) -> str:
    """
    Construye la URL para invocar el endpoint BuscarAreaAct del servicio INEGI.
    Args:
        token (str): Token de acceso al servicio INEGI.
        entidadFederativa (str, optional): Clave de la entidad federativa (por defecto "00").
        municipio (str, optional): Clave del municipio (por defecto "0").
        localidad (str, optional): Clave de la localidad (por defecto "0").
        ageb (str, optional): Clave de la AGEB (por defecto "0").
        manzana (str, optional): Clave de la manzana (por defecto "0").
        sector (str, optional): Clave del sector económico (por defecto "0").
        subsector (str, optional): Clave del subsector económico (por defecto "0").
        rama (str, optional): Clave de la rama económica (por defecto "0").
        clase (str, optional): Clave de la clase económica (por defecto "0").
        nombre (str, optional): Nombre o cadena para filtrar la actividad (por defecto "0").
        id (str, optional): Identificador específico de área de actividad (por defecto "0").
        registroInicial (int, optional): Índice del primer registro a recuperar (por defecto 1).
        offset (int, optional): Número de registros a recuperar a partir de registroInicial (por defecto 0).
    Returns:
        str: URL construida con todos los parámetros formateados listos para la solicitud.
    """
    logging.info(f"Construyendo URL INEGI: clase={clase}, registroInicial={registroInicial}, offset={offset}")
    params = BuscarAreaActParams(
        entidadFederativa=entidadFederativa,
        municipio=municipio,
        localidad=localidad,
        ageb=ageb,
        manzana=manzana,
        sector=sector,
        subsector=subsector,
        rama=rama,
        clase=clase,
        nombre=nombre,
        id=id,
        registroInicial=registroInicial,
        registroFinal=registroInicial + offset,
        token=token,
    )
    return params.url()

def generar_precio() -> float:
    """
    Genera un precio aleatorio basado en una distribución Gamma y lo ajusta a un rango específico.

    Se utiliza una distribución Gamma con parámetro shape a=10, loc=0 y scale=1000/(2**4).
    El valor muestreado se restringe al rango [100, 2000] y se redondea a dos decimales.

    Returns:
        float: Precio generado, garantizado entre 100 y 2000, con precisión de dos decimales.
    """
    precio = gamma.rvs(a=10, loc=0, scale=1000/(2**4))
    precio = max(100, min(precio, 2000))
    return round(float(precio), 2)

ACTIVIDADES_CAT = [
    "pesas libres",
    "máquinas de pesas",
    "cinta de correr",
    "elíptica",
    "spinning",
    "zumba",
    "yoga",
    "pilates",
    "HIIT",
    "crossfit",
    "entrenamiento funcional",
    "boxeo",
    "kickboxing",
    "artes marciales",
    "natación",
    "baile aeróbico",
    "entrenamiento de core",
    "entrenamiento personal",
    "circuit training",
    "estiramientos"
]
SERVICIOS_GIMNASIO = [
    "entrenamiento personal",
    "clases grupales (zumba, spinning, yoga)",
    "área de pesas libres",
    "máquinas de cardio (cinta, elíptica, remo)",
    "entrenamiento funcional y HIIT",
    "piscina y aquagym",
    "sauna y baño de vapor",
    "vestuarios con lockers",
    "toallas y servicio de bebidas",
    "evaluación física y seguimiento de progreso",
    "asesoría nutricional",
    "masajes deportivos y fisioterapia"
]

def generar_actividad() -> list[str]:
    """
    Generate a random list of activities.

    This function randomly selects between 1 and 5 activities from the predefined
    ACTIVIDADES_CAT list without replacement.

    Returns:
        list[str]: A list of strings representing the randomly selected activities.
                   Returns an empty list if num equals 0 (should not happen as the minimum is 1).
    """
    num = np.random.randint(1, 6)
    actividades = np.random.choice(ACTIVIDADES_CAT, num, replace=False) if num else []
    return [str(a) for a in actividades]

def generar_servicios() -> list[str]:
    """
    Genera una lista aleatoria de servicios para un gimnasio.
    
    La función selecciona aleatoriamente entre 1 y 4 servicios sin repetición
    de la constante SERVICIOS_GIMNASIO.
    
    Returns:
        list[str]: Lista de servicios seleccionados aleatoriamente.
                  Puede ser una lista vacía si num es 0.
    """
    num = np.random.randint(1, 5)
    servicios = np.random.choice(SERVICIOS_GIMNASIO, num, replace=False) if num else []
    return [str(s) for s in servicios]

def generar_rating() -> float:
    """
    Genera un rating aleatorio siguiendo una distribución normal.

    Esta función genera un valor de rating utilizando una distribución normal
    con media 4 y desviación estándar 0.8. El resultado está limitado al rango
    [0.1, 5.0] y se redondea a un decimal.

    Returns:
        float: Un valor de rating entre 0.1 y 5.0 con un decimal.
    """
    rating = np.random.normal(loc=4, scale=0.8)
    return round(float(max(0.1, min(rating, 5.0))), 1)

def generar_fecha_creacion() -> str:
    """
    Genera una fecha de creación aleatoria con hora ponderada.

    La fecha se elige uniformemente entre el 1 de enero de 2010 y el día anterior al actual.
    La hora del día se selecciona de 0 a 23 con la siguiente distribución de pesos:
        - Horas pico (8 a 13): peso 10
        - Horas intermedias (6-7 y 14-15): peso 5
        - Horas de la tarde (16 en adelante): peso decreciente según max(1, 24 - hora)
        - Resto de horas: peso 1

    El resultado se devuelve como una cadena con el formato "YYYY-MM-DD HH:MM:SS".

    Returns:
            str: Cadena que representa la fecha y hora generadas.
    """
    inicio = date(2010, 1, 1).toordinal()
    fin = (date.today() - timedelta(days=1)).toordinal()
    fecha = date.fromordinal(np.random.randint(inicio, fin + 1))
    horas = np.arange(24)
    pesos = np.array([10 if 8 <= h <= 13 else 5 if 6 <= h <= 7 or 14 <= h <= 15 else max(1, 24-h) if h >= 16 else 1 for h in horas], dtype=float)
    pesos /= pesos.sum()
    h = int(np.random.choice(horas, p=pesos))
    return fecha.strftime(f"%Y-%m-%d {h:02d}:%M:%S")

def mapear_datos_inegi(datos_inegi: list[dict]) -> list[dict]:
    """
    Mapea datos provenientes del INEGI a un formato estandarizado para la aplicación.

    Esta función toma una lista de diccionarios con datos del INEGI y los transforma
    a un formato consistente utilizado por la aplicación, añadiendo información generada
    (como precio, actividades, servicios, etc.) cuando sea necesario.

    Args:
        datos_inegi (list[dict]): Lista de diccionarios con datos obtenidos del INEGI,
                                 con claves como "Nombre", "Calle", "Colonia", "Ubicacion",
                                 "Longitud" y "Latitud".

    Returns:
        list[dict]: Lista de diccionarios mapeados al formato de la aplicación, con claves
                    estandarizadas como "nombre", "direccion", "ubicacion", "precio",
                    "actividades", "servicios", "averageRating", "reviewCount", "createdAt"
                    y "updatedAt".

    Nota:
        La función registra mediante logging el inicio y finalización del proceso de mapeo.
    """
    logging.info(f"Iniciando mapeo de {len(datos_inegi)} registros de INEGI.")
    mapeados = []
    for dato in datos_inegi:
        fecha = generar_fecha_creacion()
        nuevo = {
            "nombre": str(dato["Nombre"]).strip().lower(),
            "direccion": f"{dato['Calle']},{dato['Colonia']},{dato['Ubicacion']}".lower(),
            "ubicacion": [float(dato["Longitud"]), float(dato["Latitud"])],
            "precio": generar_precio(),
            "actividades": generar_actividad(),
            "servicios": generar_servicios(),
            "averageRating": generar_rating(),
            "reviewCount": -1,
            "createdAt": fecha,
            "updatedAt": fecha,
        }
        mapeados.append(nuevo)
    logging.info(f"Mapeo completado: {len(mapeados)} registros transformados.")
    return mapeados

def get_random_gyms(n: int) -> list[dict]:
    """
    Obtiene una muestra aleatoria de n gimnasios de la base de datos del INEGI.
    Esta función consulta la API del INEGI para obtener información de establecimientos
    clasificados como gimnasios (clases 713943 y 713944), y selecciona aleatoriamente
    n de ellos.
    Args:
        n (int): Número de gimnasios a obtener. Debe estar entre 1 y el total de gimnasios 
                disponibles en la base de datos.
    Returns:
        list[dict]: Lista de diccionarios, cada uno conteniendo la información de un gimnasio.
                   Los datos son transformados mediante la función mapear_datos_inegi.
    Raises:
        ValueError: Si n es menor que 1 o mayor que el total de gimnasios disponibles.
    Nota:
        Requiere que la variable de entorno TOKEN_INEGI esté configurada con un token válido.
        La función utiliza ThreadPoolExecutor para realizar consultas paralelas a la API.
    """
    MAX_REG = {"713944": 269, "713943": 2003}
    total_disponible = sum(MAX_REG.values())
    logging.info(f"Petición de {n} gimnasios (disponibles: {total_disponible}).")
    if n < 1 or n > total_disponible:
        raise ValueError(f"El parámetro n debe estar entre 1 y {total_disponible}.")

    token = os.getenv("TOKEN_INEGI")
    logging.info("Token INEGI obtenido de entorno.")
    datos: list[dict] = []

    def fetch_data(clase: str) -> list[dict]:
        url = build_buscar_area_act_url(
            token=token,
            entidadFederativa="09",
            municipio="0",
            localidad="0",
            ageb="0",
            manzana="0",
            sector="0",
            subsector="0",
            rama="0",
            clase=clase,
            nombre="0",
            id="0",
            registroInicial=0,
            offset=MAX_REG[clase],
        )
        logging.info(f"Solicitando datos INEGI para clase {clase}.")
        resp = requests.get(url)
        if resp.status_code != 200:
            logging.warning(f"INEGI API devolvió status {resp.status_code} para clase {clase}.")
        data = resp.json()
        logging.info(f"Clase {clase}: obtenidos {len(data)} registros.")
        return data

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(MAX_REG)) as executor:
        for batch in executor.map(fetch_data, MAX_REG.keys()):
            datos.extend(batch)

    logging.info(f"Total bruto registros INEGI recolectados: {len(datos)}.")
    n = min(n, len(datos))
    datos_muestra = np.random.choice(datos, n, replace=False).tolist()
    muestra = mapear_datos_inegi(datos_muestra)

    logging.info("Muestra de gimnasios generada.")
    return muestra

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Obtiene una muestra aleatoria de gimnasios de INEGI."
    )
    parser.add_argument(
        "-n", type=int, required=True,
        help="Número de gimnasios a recuperar."
    )
    parser.add_argument(
        "-o", "--output", default="gyms.json",
        help="Archivo de salida (por defecto: gyms.json)."
    )
    args = parser.parse_args()

    logging.info("Iniciando proceso ETL de gimnasios.")
    resultado = get_random_gyms(args.n)

    logging.info(f"Guardando resultado en '{args.output}'.")
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)
    logging.info("Proceso completado correctamente.")
