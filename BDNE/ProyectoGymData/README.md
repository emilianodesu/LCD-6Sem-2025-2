# bdne - ETL and Data Integration

Este repositorio contiene scripts para extraer, transformar y cargar (ETL) datos de distintas fuentes—INEGI (gimnasios), Mockaroo (usuarios) y MongoDB (reseñas)—y luego combinarlos e insertar en una base de datos MongoDB única.

## Entorno Virtual
```bash
# Crear y activar el entorno virtual
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Linux/MacOS
source .venv/bin/activate

# Actualizar pip e instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

## Índice

- [bdne - ETL and Data Integration](#bdne---etl-and-data-integration)
  - [Entorno Virtual](#entorno-virtual)
  - [Índice](#índice)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Requisitos](#requisitos)
  - [Variables de entorno](#variables-de-entorno)
  - [Instalación](#instalación)
  - [Uso de los ETLs individuales](#uso-de-los-etls-individuales)
    - [Gyms.py](#gymspy)
    - [Users.py](#userspy)
    - [Reviews.py](#reviewspy)
  - [Integración de datos](#integración-de-datos)
    - [integracion.py](#integracionpy)
  - [Carga en MongoDB](#carga-en-mongodb)
  - [Índices y colecciones](#índices-y-colecciones)
  - [Presentacion](#presentacion)

## Estructura del proyecto

```
bdne/
├── Gyms.py           # ETL de gimnasios desde INEGI
├── Users.py          # ETL de usuarios simulados desde Mockaroo y geocodificación
├── Reviews.py        # ETL de reseñas desde colecciones MongoDB
├── integracion.py    # Orquestador que combina y carga todos los datos en MongoDB
├── requirements.txt  # Dependencias de Python
├── alcaldias/        # Shape files para delimitación geográfica de alcaldías CDMX
└── initdb/           # Scripts de inicialización y creación de colecciones/índices
└── presentacion/     # Es una parte desglosada de las sentencias que se encuentran en initdb
```

## Requisitos

- Python 3.8+
- MongoDB (para pruebas locales o conexión a un clúster remoto)
- Credenciales y tokens:
  - INEGI API Token
  - Mockaroo API Key
  - MongoDB URI (para lectura y escritura)

## Variables de entorno

Coloca un archivo `.env` en la raíz del proyecto con al menos las siguientes variables:

```dotenv
TOKEN_INEGI=tu_token_inegi
MOCKARO_KEY=tu_clave_mockaroo
MONGO_URI=mongodb://usuario:password@host:puerto/bd?authSource=admin
MONGO_URI_BULK=mongodb://usuario:password@host:puerto/bd_bulk?authSource=admin
```

## Instalación

```powershell
# Crear entorno virtual (opcional)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

## Uso de los ETLs individuales

### Gyms.py

Extrae datos de establecimientos (clase 713943 y 713944) desde la API de INEGI y los transforma a un esquema estándar.

```powershell
python Gyms.py -n <número_de_gimnasios> -o gyms.json
```

- `-n`: número de registros a recuperar.
- `-o`: archivo de salida (por defecto `gyms.json`).

### Users.py

Genera usuarios simulados para CDMX usando Mockaroo y shapefile de alcaldías, distribuyendo coordenadas dentro de polígonos.

```powershell
python Users.py --num <cantidad> --path users.json
```

- `--num`: número de usuarios (mínimo 2).
- `--path`: archivo de salida (por defecto `users.json`).

### Reviews.py

Recupera citas y reseñas de tres colecciones en MongoDB y genera un muestreo aleatorio.

```powershell
python Reviews.py --num <cantidad> --path reviews.json
```

- `--num`: número de reseñas (por defecto 10).
- `--path`: archivo de salida (por defecto `reviews.json`).

## Integración de datos

### integracion.py

Este script orquesta la ejecución concurrente de los tres ETLs anteriores y carga los resultados en MongoDB.

```powershell
python integracion.py --iterations <veces> --num-gyms <G> --num-reviews <R> --num-users <U>
```

- `--iterations`: cuántas veces repetir el proceso completo (por defecto 1).
- `--num-gyms`: número de gimnasios a generar por iteración (por defecto 50).
- `--num-reviews`: número de reseñas por iteración (por defecto 200).
- `--num-users`: número de usuarios por iteración (por defecto 400).

El flujo interno realiza:
1. Extracción y transformación concurrente de gimnasios, reseñas y usuarios.
2. Inserción de usuarios (roles `user` y `owner`) en `users`.
3. Inserción de gimnasios en `gyms`, asignando owners aleatoriamente.
4. Inserción de reviews en `reviews` y actualización de contadores (`reviewCount`).
5. Generación de relaciones de favoritos y followers entre usuarios y gimnasios.

## Carga en MongoDB

- Usa `MONGO_URI` para los ETLs de `Reviews.py` y `Users.py`.
- Usa `MONGO_URI_BULK` en `integracion.py` para operaciones bulk.

## Índices y colecciones

En `initdb/` encontrarás scripts para crear:

- Colección `users`
- Colección `gyms`
- Colección `reviews`
- Índices GeoJSON para búsquedas espaciales
- Índices de campo para optimizar consultas por fecha y rating

Además, en la carpeta `presentacion/` se incluyen los mismos scripts desglosados paso a paso, mostrando cada sentencia de inicialización del esquema de la base de datos para fines de presentación y documentación detallada.

Puedes aplicar estos scripts desde la shell de MongoDB:

```powershell
mongo <ruta>/initdb/01-creacion-coleccion-user.js
mongo <ruta>/initdb/02-creacion-coleccion-gyms.js
# ... etc.
```

## Presentacion
En la carpeta se encuentran las sentencias para crear las colecciones e indices que conforman a la base de datos