# Sección: Integracion
# Sección: prelude

import pandas as pd
import itables
import unicodedata
import sqlite3
import pandas as pd
import missingno as msno
from ydata_profiling import ProfileReport
import matplotlib.pyplot as plt
import sqlite3
import sqlite3
import pandas as pd
import recordlinkage
import itables


wb = pd.read_csv("../wb/WB_ESG.csv")
itables.show(wb)

def estandarizar_texto(texto):
    if pd.isna(texto):
        return ''
    s = str(texto)
    nkfd = unicodedata.normalize('NFKD', s)
    sin_acentos = ''.join(c for c in nkfd if not unicodedata.combining(c))
    sin_espacios = sin_acentos.replace(" ", "_")
    return sin_espacios.upper()
def filtrar_wb(wb: pd.DataFrame) -> pd.DataFrame:
    wb_ = wb[wb['REF_AREA_LABEL'] == 'United States'].copy()
    wb_ = wb_.dropna()
    return wb_
def filtrar_unpd(df  : pd.DataFrame) -> pd.DataFrame:
    df_ = df[df['Location'].isin(['United States of America'])].copy()
    df_ = df_.dropna()
    return df_
def dataframe_to_sql(wb: pd.DataFrame,table:str='INDICADOR_UNIFICADO') -> str:
    cols = wb.columns.tolist()
    rows_sql = []
    for _, row in wb.iterrows():
        vals = []
        for c in cols:
            v = row[c]
            if isinstance(v, str):
                v = v.replace("'", "''")
                vals.append(f"'{v}'")
            else:
                vals.append(str(v))
        rows_sql.append(f"({', '.join(vals)})")

    cols_sql = ', '.join(f'"{c}"' for c in cols)
    values_sql = ',\n'.join(rows_sql)
    return f'INSERT INTO {table} ({cols_sql}) VALUES\n{values_sql};'
def clear_db(path: str):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS INDICADOR_UNIFICADO")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS INDICADOR_UNIFICADO (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fuente TEXT NOT NULL CHECK (
                fuente IN ('WORLD_BANK', 'UNDP')
            ),
            nombre TEXT NOT NULL,
            unidad_medida TEXT NULL,
            tipo_medida TEXT NULL,
            valor REAL NOT NULL,
            anio INTEGER NOT NULL,
            edad_inicio INTEGER NULL,
            edad_fin INTEGER NULL
        );
    ''')
    conn.commit()
    conn.close()
clear_db('main.db')

rutas_poblacion_unpd = [
    "p1.csv",
    "p2.csv",
    "p3.csv",
    "p4.csv",
    "p5.csv",
]
rutas_mortalidad_unpd = [
    "m1.csv",
    "m2.csv",
    "m3.csv",
    "m4.csv",
]
rutas_familia_unpd = [
    "f1.csv",
    "f2.csv",
    "f3.csv",
    "f4.csv",
    "f5.csv",
]
rutas_planeacion_familiar_unpd = [
    "fp1.csv",
]
# agregar prefijos
rutas_poblacion_unpd = [f"../unpd/{ruta}" for ruta in rutas_poblacion_unpd]
rutas_mortalidad_unpd = [f"../unpd/{ruta}" for ruta in rutas_mortalidad_unpd]
rutas_familia_unpd = [f"../unpd/{ruta}" for ruta in rutas_familia_unpd]
rutas_planeacion_familiar_unpd = [f"../unpd/{ruta}" for ruta in rutas_planeacion_familiar_unpd]
unpd = []
unpd.extend(
    rutas_familia_unpd + rutas_mortalidad_unpd + rutas_poblacion_unpd + rutas_planeacion_familiar_unpd
)
# Cargar y estandarizar los datos de UNPD
dfs = []
for ruta in unpd:
    df = pd.read_csv(ruta, usecols=['Location','AgeStart','AgeEnd','Time','Value','IndicatorShortName'])
    df = filtrar_unpd(df) 
    df['location'] = df['Location'].apply(
        lambda x: unicodedata.normalize('NFKD', str(x))
                            .encode('ascii', 'ignore')
                            .decode('ascii')
                            .upper()
    )
    dfs.append(df)
unpd_dfs = pd.concat(dfs, ignore_index=True)

unpd_dfs['nombre'] = unpd_dfs['IndicatorShortName'].apply(estandarizar_texto)
unpd_dfs['valor'] = unpd_dfs['Value']
unpd_dfs['anio'] = unpd_dfs['Time']
unpd_dfs['edad_inicio'] = unpd_dfs['AgeStart']
unpd_dfs['edad_fin'] = unpd_dfs['AgeEnd']
unpd_dfs = unpd_dfs[['nombre', 'valor', 'anio', 'edad_inicio', 'edad_fin']]
unpd_dfs['fuente'] = 'UNDP'
unpd_dfs = unpd_dfs.dropna()

itables.show(unpd_dfs)

wb_clean = wb.copy()
wb_clean = filtrar_wb(wb_clean)
wb_clean = wb_clean[['INDICATOR_LABEL', 'UNIT_MEASURE_LABEL', 'UNIT_TYPE', 'OBS_VALUE', 'TIME_PERIOD', 'REF_AREA_LABEL']]
wb_clean['nombre'] = wb_clean['INDICATOR_LABEL'].apply(estandarizar_texto)
wb_clean['unidad_medida'] = wb_clean['UNIT_MEASURE_LABEL'].apply(estandarizar_texto)
wb_clean['tipo_medida'] = wb_clean['UNIT_TYPE'].apply(estandarizar_texto)
wb_clean['valor'] = wb_clean['OBS_VALUE']
wb_clean['anio'] = wb_clean['TIME_PERIOD']
wb_clean = wb_clean[['nombre', 'unidad_medida', 'tipo_medida', 'valor', 'anio']]
wb_clean = wb_clean.dropna()
wb_clean['fuente'] = 'WORLD_BANK'
itables.show(wb_clean)

unpd_canonical = dataframe_to_sql(unpd_dfs)
print(unpd_canonical)

wb_canonical = dataframe_to_sql(wb_clean)
print(wb_canonical)

# cargar los datos en la base de datos
conn = sqlite3.connect('main.db')
cursor = conn.cursor()
cursor.executescript(unpd_canonical)
cursor.executescript(wb_canonical)
conn.commit()
conn.close()

conn = sqlite3.connect('main.db')
df = pd.read_sql_query("SELECT * FROM INDICADOR_UNIFICADO", conn)
print(df.shape)
itables.show(df)
conn.close()

