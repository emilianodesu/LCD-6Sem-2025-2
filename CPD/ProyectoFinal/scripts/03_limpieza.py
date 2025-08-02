# Sección: Limpieza
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


conn = sqlite3.connect(r"./main.db")
query = "SELECT * FROM INDICADOR_UNIFICADO"
df_unificado = pd.read_sql_query(query, conn)
conn.close()

print("Registros cargados:", len(df_unificado))
df_unificado.head()

absolutos = [
    'LIVE_BIRTHS_BY_AGE_OF_MOTHER_(AND_SEX_OF_CHILD)_-_COMPLETE',
    'DEATHS_BY_AGE_AND_SEX_-_COMPLETE',
    'TOTAL_DEATHS_BY_SEX',
    'TOTAL_POPULATION_BY_SEX',
    'NET_MIGRATION',
    'NATURAL_CHANGE_OF_POPULATION',
    'TREE_COVER_LOSS_(HECTARES)',
    'SCIENTIFIC_AND_TECHNICAL_JOURNAL_ARTICLES',
    'PATENT_APPLICATIONS,_RESIDENTS',
    'GHG_NET_EMISSIONS/REMOVALS_BY_LUCF_(MT_OF_CO2_EQUIVALENT)'
]

df_absolutos = df_unificado[df_unificado['nombre'].isin(absolutos)].copy()
df_absolutos.head()

df_absolutos['edad_inicio'] = pd.to_numeric(df_absolutos['edad_inicio'], errors='coerce')
df_absolutos['edad_fin'] = pd.to_numeric(df_absolutos['edad_fin'], errors='coerce')

# Calcular la diferencia de edad
diferencia = df_absolutos['edad_fin'] - df_absolutos['edad_inicio']

# Condiciones
cond_misma_edad = (diferencia >= 0) & (diferencia <= 1)
cond_no_importa_edad = (diferencia > 1) | (diferencia < 0) | (df_absolutos['edad_inicio'].isna()) | (df_absolutos['edad_fin'].isna())

# Dividir en los dos DataFrames
df_absolutos_misma_edad = df_absolutos[cond_misma_edad].copy()
df_absolutos_no_importa_edad = df_absolutos[cond_no_importa_edad].copy()

df_absolutos_misma_edad = df_absolutos_misma_edad.drop(columns=['edad_fin'])
df_absolutos_misma_edad = df_absolutos_misma_edad.rename(columns={'edad_inicio': 'edad'})
df_absolutos_no_importa_edad = df_absolutos_no_importa_edad.drop(columns=['edad_inicio', 'edad_fin'])

df_absolutos_no_importa_edad = df_absolutos_no_importa_edad[df_absolutos_no_importa_edad['anio'] <= 2025]
df_absolutos_misma_edad = df_absolutos_misma_edad[df_absolutos_misma_edad['anio'] <= 2025]

df_absolutos_misma_edad.loc[:, 'unidad_medida'] = df_absolutos_misma_edad['unidad_medida'].fillna("Desconocido")
df_absolutos_misma_edad.loc[:, 'tipo_medida'] = df_absolutos_misma_edad['tipo_medida'].fillna("Desconocido")

df_absolutos_no_importa_edad.loc[:, 'unidad_medida'] = df_absolutos_no_importa_edad['unidad_medida'].fillna("Desconocido")
df_absolutos_no_importa_edad.loc[:, 'tipo_medida'] = df_absolutos_no_importa_edad['tipo_medida'].fillna("Desconocido")

# Misma edad
df_absolutos_misma_edad.loc[:, 'nombre'] = df_absolutos_misma_edad['nombre'].str.strip().str.title()
df_absolutos_misma_edad.loc[:, 'unidad_medida'] = df_absolutos_misma_edad['unidad_medida'].str.lower().str.strip()
df_absolutos_misma_edad.loc[:, 'tipo_medida'] = df_absolutos_misma_edad['tipo_medida'].str.lower().str.strip()

# No importa edad
df_absolutos_no_importa_edad.loc[:, 'nombre'] = df_absolutos_no_importa_edad['nombre'].str.strip().str.title()
df_absolutos_no_importa_edad.loc[:, 'unidad_medida'] = df_absolutos_no_importa_edad['unidad_medida'].str.lower().str.strip()
df_absolutos_no_importa_edad.loc[:, 'tipo_medida'] = df_absolutos_no_importa_edad['tipo_medida'].str.lower().str.strip()

df_absolutos_no_importa_edad.head()

df_absolutos_misma_edad.head()

def detectar_duplicados_por_lotes(df, batch_size=1000):
    duplicados_ids = set()
    for start in range(0, len(df), batch_size):
        end = start + batch_size
        df_lote = df.iloc[start:end]

        indexer = recordlinkage.Index()
        indexer.full()
        candidate_links = indexer.index(df_lote)

        compare = recordlinkage.Compare()
        compare.string('nombre', 'nombre', method='jarowinkler', threshold=0.95, label='nombre_similar')
        compare.exact('anio', 'anio', label='anio_igual')
        compare.numeric('valor', 'valor', offset=0.01, scale=1.0, label='valor_cercano')
        compare.numeric('edad', 'edad', offset=1, scale=1.0, label='edad_cercano')

        features = compare.compute(candidate_links, df_lote)
        features['score_total'] = features.sum(axis=1)
        duplicados = features[features["score_total"] >= 4].index
        duplicados_ids.update(i for i, _ in duplicados)

    return df.drop(index=duplicados_ids, errors='ignore')

# Ejecutar
df_absolutos_limpio_edad = detectar_duplicados_por_lotes(df_absolutos_misma_edad)

bins = [0, 5, 12, 18, 30, 60, 100]
labels = ['Bebé', 'Niñez', 'Adolescencia', 'Joven', 'Adulto', 'Mayor']
df_absolutos_limpio_edad['edad_grupo'] = pd.cut(df_absolutos_limpio_edad['edad'], bins=bins, labels=labels)

df_absolutos_limpio_edad['valor_norm'] = df_absolutos_limpio_edad.groupby('nombre')['valor'].transform(
    lambda x: (x - x.min()) / (x.max() - x.min())
)
itables.show(df_absolutos_limpio_edad)

df_absolutos_no_importa_edad['valor_norm'] = df_absolutos_no_importa_edad.groupby('nombre')['valor'].transform(
    lambda x: (x - x.min()) / (x.max() - x.min())
)
itables.show(df_absolutos_no_importa_edad)

# Generar el archivo CSV
df_absolutos_limpio_edad.to_csv('./cleaned_data/absolutos_misma_edad.csv', index=False)
df_absolutos_no_importa_edad.to_csv('./cleaned_data/absolutos_no_importa_edad.csv', index=False)

indices = [
    'CRUDE_BIRTH_RATE_(BIRTHS_PER_1,000_POPULATION)',
    'SEX_RATIO_AT_BIRTH_(PER_FEMALE_NEWBORN)',
    'TOTAL_FERTILITY_RATE',
    'LIFE_EXPECTANCY_AT_EXACT_AGES,_EX,_BY_SINGLE_AGE_AND_BY_SEX',
    'CHILD_DEPENDENCY_RATIO',
    'OLD-AGE_DEPENDENCY_RATIO',
    'POPULATION_DENSITY_(PERSONS_PER_SQUARE_KM)',
    'POPULATION_DENSITY_(PEOPLE_PER_SQ._KM_OF_LAND_AREA)',
    'CONTRACEPTIVE_USERS',
    'AGRICULTURAL_LAND_(%_OF_LAND_AREA)',
    'FOREST_AREA_(%_OF_LAND_AREA)',
    'FOOD_PRODUCTION_INDEX_(2014-2016_=_100)',
    'CONTROL_OF_CORRUPTION:_ESTIMATE',
    'ACCESS_TO_CLEAN_FUELS_AND_TECHNOLOGIES_FOR_COOKING_(%_OF_POPULATION)',
    'ENERGY_INTENSITY_LEVEL_OF_PRIMARY_ENERGY_(MJ/$2017_PPP_GDP)',
    'ACCESS_TO_ELECTRICITY_(%_OF_POPULATION)',
    'ELECTRICITY_PRODUCTION_FROM_COAL_SOURCES_(%_OF_TOTAL)',
    'RENEWABLE_ELECTRICITY_OUTPUT_(%_OF_TOTAL_ELECTRICITY_OUTPUT)',
    'RENEWABLE_ENERGY_CONSUMPTION_(%_OF_TOTAL_FINAL_ENERGY_CONSUMPTION)',
    'ENERGY_IMPORTS,_NET_(%_OF_ENERGY_USE)',
    'FOSSIL_FUEL_ENERGY_CONSUMPTION_(%_OF_TOTAL)',
    'ENERGY_USE_(KG_OF_OIL_EQUIVALENT_PER_CAPITA)',
    'PM2.5_AIR_POLLUTION,_MEAN_ANNUAL_EXPOSURE_(MICROGRAMS_PER_CUBIC_METER)',
    'STANDARDISED_PRECIPITATION-EVAPOTRANSPIRATION_INDEX',
    'PROPORTION_OF_BODIES_OF_WATER_WITH_GOOD_AMBIENT_WATER_QUALITY',
    'LEVEL_OF_WATER_STRESS:_FRESHWATER_WITHDRAWAL_AS_A_PROPORTION_OF_AVAILABLE_FRESHWATER_RESOURCES',
    'TERRESTRIAL_AND_MARINE_PROTECTED_AREAS_(%_OF_TOTAL_TERRITORIAL_AREA)',
    'RESEARCH_AND_DEVELOPMENT_EXPENDITURE_(%_OF_GDP)',
    'GOVERNMENT_EFFECTIVENESS:_ESTIMATE',
    'STRENGTH_OF_LEGAL_RIGHTS_INDEX_(0=WEAK_TO_12=STRONG)',
    'INDIVIDUALS_USING_THE_INTERNET_(%_OF_POPULATION)',
    'AGRICULTURE,_FORESTRY,_AND_FISHING,_VALUE_ADDED_(%_OF_GDP)',
    'ADJUSTED_SAVINGS:_NET_FOREST_DEPLETION_(%_OF_GNI)',
    'ADJUSTED_SAVINGS:_NATURAL_RESOURCES_DEPLETION_(%_OF_GNI)',
    'GDP_GROWTH_(ANNUAL_%)',
    'POLITICAL_STABILITY_AND_ABSENCE_OF_VIOLENCE/TERRORISM:_ESTIMATE',
    'RULE_OF_LAW:_ESTIMATE',
    'REGULATORY_QUALITY:_ESTIMATE',
    'ECONOMIC_AND_SOCIAL_RIGHTS_PERFORMANCE_SCORE',
    'SCHOOL_ENROLLMENT,_PRIMARY_AND_SECONDARY_(GROSS),_GENDER_PARITY_INDEX_(GPI)',
    'SCHOOL_ENROLLMENT,_PRIMARY_(%_GROSS)',
    'GOVERNMENT_EXPENDITURE_ON_EDUCATION,_TOTAL_(%_OF_GOVERNMENT_EXPENDITURE)',
    'PROPORTION_OF_SEATS_HELD_BY_WOMEN_IN_NATIONAL_PARLIAMENTS_(%)',
    'CAUSE_OF_DEATH,_BY_COMMUNICABLE_DISEASES_AND_MATERNAL,_PRENATAL_AND_NUTRITION_CONDITIONS_(%_OF_TOTAL)',
    'MORTALITY_RATE,_UNDER-5_(PER_1,000_LIVE_BIRTHS)',
    'PEOPLE_USING_SAFELY_MANAGED_DRINKING_WATER_SERVICES_(%_OF_POPULATION)',
    'PEOPLE_USING_SAFELY_MANAGED_SANITATION_SERVICES_(%_OF_POPULATION)',
    'INCOME_SHARE_HELD_BY_LOWEST_20%',
    'GINI_INDEX',
    'ANNUALIZED_AVERAGE_GROWTH_RATE_IN_PER_CAPITA_REAL_SURVEY_MEAN_CONSUMPTION_OR_INCOME,_TOTAL_POPULATION_(%)',
    'LABOR_FORCE_PARTICIPATION_RATE,_TOTAL_(%_OF_TOTAL_POPULATION_AGES_15-64)_(MODELED_ILO_ESTIMATE)',
    'RATIO_OF_FEMALE_TO_MALE_LABOR_FORCE_PARTICIPATION_RATE_(%)_(MODELED_ILO_ESTIMATE)',
    'UNEMPLOYMENT,_TOTAL_(%_OF_TOTAL_LABOR_FORCE)_(MODELED_ILO_ESTIMATE)',
    'PREVALENCE_OF_UNDERNOURISHMENT_(%_OF_POPULATION)',
    'LIFE_EXPECTANCY_AT_BIRTH,_TOTAL_(YEARS)',
    'FERTILITY_RATE,_TOTAL_(BIRTHS_PER_WOMAN)',
    'UNMET_NEED_FOR_CONTRACEPTION_(%_OF_MARRIED_WOMEN_AGES_15-49)',
    'VOICE_AND_ACCOUNTABILITY:_ESTIMATE',
    'HOSPITAL_BEDS_(PER_1,000_PEOPLE)', 
    'POPULATION_AGES_65_AND_ABOVE_(%_OF_TOTAL_POPULATION)',  
    'ANNUAL_FRESHWATER_WITHDRAWALS,_TOTAL_(%_OF_INTERNAL_RESOURCES)',  
    'CO2_EMISSIONS_(METRIC_TONS_PER_CAPITA)', 
    'METHANE_EMISSIONS_(METRIC_TONS_OF_CO2_EQUIVALENT_PER_CAPITA)',  
    'NITROUS_OXIDE_EMISSIONS_(METRIC_TONS_OF_CO2_EQUIVALENT_PER_CAPITA)'  
]

df_indices = df_unificado[df_unificado['nombre'].isin(indices)]
df_indices.head()

df_indices.loc[:, 'edad_inicio'] = pd.to_numeric(df_indices['edad_inicio'], errors='coerce')
df_indices.loc[:, 'edad_fin'] = pd.to_numeric(df_indices['edad_fin'], errors='coerce')

# Calcular la diferencia de edad
diferencia = df_indices['edad_fin'] - df_indices['edad_inicio']

# Condiciones
cond_misma_edad = (diferencia >= 0) & (diferencia <= 1)
cond_no_importa_edad = (diferencia > 1) | (diferencia < 0) | (df_indices['edad_inicio'].isna()) | (df_indices['edad_fin'].isna())

# Dividir en los dos DataFrames
df_indices_misma_edad = df_indices[cond_misma_edad].copy()
df_indices_no_importa_edad = df_indices[cond_no_importa_edad].copy()

df_indices_misma_edad = df_indices_misma_edad.drop(columns=['edad_fin'])
df_indices_misma_edad = df_indices_misma_edad.rename(columns={'edad_inicio': 'edad'})
df_indices_no_importa_edad = df_indices_no_importa_edad.drop(columns=['edad_inicio', 'edad_fin'])
df_indices_no_importa_edad = df_indices_no_importa_edad[df_indices_no_importa_edad['anio'] <= 2025]
df_indices_misma_edad = df_indices_misma_edad[df_indices_misma_edad['anio'] <= 2025]

# Rellenar nulos
df_indices_misma_edad.loc[:, 'unidad_medida'] = df_indices_misma_edad['unidad_medida'].fillna("Desconocido")
df_indices_misma_edad.loc[:, 'tipo_medida'] = df_indices_misma_edad['tipo_medida'].fillna("Desconocido")
df_indices_no_importa_edad.loc[:, 'unidad_medida'] = df_indices_no_importa_edad['unidad_medida'].fillna("Desconocido")
df_indices_no_importa_edad.loc[:, 'tipo_medida'] = df_indices_no_importa_edad['tipo_medida'].fillna("Desconocido")

# Limpiar texto
df_indices_misma_edad.loc[:, 'nombre'] = df_indices_misma_edad['nombre'].str.strip().str.title()
df_indices_misma_edad.loc[:, 'unidad_medida'] = df_indices_misma_edad['unidad_medida'].str.lower().str.strip()
df_indices_misma_edad.loc[:, 'tipo_medida'] = df_indices_misma_edad['tipo_medida'].str.lower().str.strip()

df_indices_no_importa_edad.loc[:, 'nombre'] = df_indices_no_importa_edad['nombre'].str.strip().str.title()
df_indices_no_importa_edad.loc[:, 'unidad_medida'] = df_indices_no_importa_edad['unidad_medida'].str.lower().str.strip()
df_indices_no_importa_edad.loc[:, 'tipo_medida'] = df_indices_no_importa_edad['tipo_medida'].str.lower().str.strip()

df_indices_misma_edad['valor_norm'] = df_indices_misma_edad.groupby('nombre')['valor'].transform(
    lambda x: (x - x.min()) / (x.max() - x.min())
)
itables.show(df_indices_misma_edad)

df_indices_no_importa_edad['valor_norm'] = df_indices_no_importa_edad.groupby('nombre')['valor'].transform(
    lambda x: (x - x.min()) / (x.max() - x.min())
)
itables.show(df_indices_no_importa_edad)

# Generar el archivo CSV
df_indices_misma_edad.to_csv('./cleaned_data/indices_misma_edad.csv', index=False)
df_indices_no_importa_edad.to_csv('./cleaned_data/indices_no_importa_edad.csv', index=False)

