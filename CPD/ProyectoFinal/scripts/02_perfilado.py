# Sección: Perfilado
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


conn = sqlite3.connect('main.db')
# Cargar a DataFrame
query = "SELECT * FROM INDICADOR_UNIFICADO"
df_unificado = pd.read_sql_query(query, conn)
conn.close()

# Mostrar las primeras filas para verificar
print("Registros cargados:", len(df_unificado))
df_unificado.head()

df_unificado.head()

df_unificado.tail()

print("Valores nulos por columna (TOTAL):\n", df_unificado.isnull().sum())
print("\nTipos de datos:\n", df_unificado.dtypes)
print("\nFuentes únicas:", df_unificado['fuente'].unique())
print("\nnombres únicos:", df_unificado['nombre'].unique())
print("\nAños únicos:", sorted(df_unificado['anio'].unique()))

profile = ProfileReport(
    df_unificado,
    title="Reporte de Perfilado - Datos UNPD y Banco Mundial UNIFICADOS",
    explorative=True,  
    correlations={
        "pearson": {"calculate": True},
        "spearman": {"calculate": True},
        "kendall": {"calculate": True},
        "phi_k": {"calculate": True},
    },
    missing_diagrams={
        "bar": True,
        "matrix": True,
        "heatmap": True,
    },
)

# Guardar como HTML
profile.to_file("reporte_perfilado_unificado.html")
print("\nReporte generado: 'reporte_perfilado_unificado.html'")

# Ya se vieron los faltantes pero obtenemos un promedio
completitud = df_unificado.notna().mean() * 100
print("Porcentaje de completitud por columna:\n", completitud)

msno.bar(df_unificado, figsize=(10, 4))

# Valores únicos para las categóricas
#print("Fuentes únicas:", df_unificado['fuente'].unique())
#print("\nUnidades de medida:", df_unificado['unidad_medida'].unique())
#print("\nnombre:", df_unificado['nombre'].unique())
#print("\nTipo de medida:", df_unificado['tipo_medida'].unique())

# Verificar rangos numéricos
print("\nRango de años:", df_unificado['anio'].min(), "-", df_unificado['anio'].max())
print("\nRango de valores:", df_unificado['valor'].describe()[['min', 'max']])

# Inconsistencias en rangos de edad (UNDP)
if 'edad_inicio' in df_unificado.columns:
    edades_invalidas = df_unificado[(df_unificado['edad_inicio'] < 0) | (df_unificado['edad_inicio'] > 100)]
    print("\nRegistros con edades inválidas:", len(edades_invalidas))

# inconsistencias respecto a año
futuros = df_unificado[df_unificado['anio'] > 2024]
print(f"\nRegistros con año posterior a 2024: {len(futuros)}")

"""
if len(futuros) > 0:
    print("\nEjemplo de registros inconsistentes (valores en años futuros):")
    display(futuros[['fuente', 'nombre', 'valor', 'anio']].head())
"""

duplicados_exactos = df_unificado[df_unificado.duplicated(keep=False)]  

print(f"Número de registros duplicados exactos: {len(duplicados_exactos)}")
if not duplicados_exactos.empty:
    print("\nEjemplo de registros duplicados:")
    display(duplicados_exactos.sort_values(by=list(df_unificado.columns)).head())

columnas_clave = ['nombre', 'valor', 'anio']  
duplicados_parciales = df_unificado[df_unificado.duplicated(subset=columnas_clave, keep=False)]

print(df_unificado.shape)
print(f"\nNúmero de registros duplicados (parciales en {columnas_clave}): {len(duplicados_parciales)}")
"""
if not duplicados_parciales.empty:
    print("\nEjemplo de duplicados parciales:")
    display(duplicados_parciales.sort_values(by=columnas_clave).head())
"""

conteo_duplicados = df_unificado.groupby(columnas_clave).size().reset_index(name='conteo')
conteo_duplicados = conteo_duplicados[conteo_duplicados['conteo'] > 1]

print("\nRegistros con más de una ocurrencia:")
#print(conteo_duplicados.sort_values('conteo', ascending=False))
conteo_duplicados.sort_values('conteo', ascending=False)

# Detección de outliers en 'valor' (método IQR)
Q1 = df_unificado['valor'].quantile(0.25)
Q3 = df_unificado['valor'].quantile(0.75)
IQR = Q3 - Q1
outliers = df_unificado[(df_unificado['valor'] < (Q1 - 1.5*IQR)) | (df_unificado['valor'] > (Q3 + 1.5*IQR))]
print("\nNúmero de outliers en 'valor':", len(outliers))

import seaborn as sns
sns.boxplot(x=df_unificado['valor'])

outliers_por_anio = df_unificado.groupby('anio')['valor'].apply(
    lambda x: x[(x < (x.quantile(0.25) - 1.5 * (x.quantile(0.75) - x.quantile(0.25)))) | 
                (x > (x.quantile(0.75) + 1.5 * (x.quantile(0.75) - x.quantile(0.25))))]
)

# Conteo de outliers por año
print("Número de outliers por año:")
print(outliers_por_anio.groupby('anio').size())

# Filtrar outliers
outliers = df_unificado[
    (df_unificado['valor'] < (Q1 - 1.5 * IQR)) | 
    (df_unificado['valor'] > (Q3 + 1.5 * IQR))
][['nombre', 'valor', 'anio']]

print(f"\n {len(outliers)} outliers en 'valor':")
print(outliers.sort_values(by='valor', ascending=False))

absolutos = [
    'LIVE_BIRTHS_BY_AGE_OF_MOTHER_(AND_SEX_OF_CHILD)_-_COMPLETE',
    'DEATHS_BY_AGE_AND_SEX_-_COMPLETE',
    'TOTAL_DEATHS_BY_SEX',
    'TOTAL_POPULATION_BY_SEX',
    'NET_MIGRATION',
    'NATURAL_CHANGE_OF_POPULATION',
    'TREE_COVER_LOSS_(HECTARES)',
    'CO2_EMISSIONS_(METRIC_TONS_PER_CAPITA)',
    'METHANE_EMISSIONS_(METRIC_TONS_OF_CO2_EQUIVALENT_PER_CAPITA)',
    'NITROUS_OXIDE_EMISSIONS_(METRIC_TONS_OF_CO2_EQUIVALENT_PER_CAPITA)',
    'GHG_NET_EMISSIONS/REMOVALS_BY_LUCF_(MT_OF_CO2_EQUIVALENT)',
    'ANNUAL_FRESHWATER_WITHDRAWALS,_TOTAL_(%_OF_INTERNAL_RESOURCES)',
    'SCIENTIFIC_AND_TECHNICAL_JOURNAL_ARTICLES',
    'PATENT_APPLICATIONS,_RESIDENTS',
    'HOSPITAL_BEDS_(PER_1,000_PEOPLE)',
    'POPULATION_AGES_65_AND_ABOVE_(%_OF_TOTAL_POPULATION)'  
]

df_absolutos = df_unificado[df_unificado['nombre'].isin(absolutos)]
df_absolutos.head()

# Cálculo de IQR
Q1_abs = df_absolutos['valor'].quantile(0.25)
Q3_abs = df_absolutos['valor'].quantile(0.75)
IQR_abs = Q3_abs - Q1_abs

# Detección de outliers
outliers_abs = df_absolutos[
    (df_absolutos['valor'] < (Q1_abs - 1.5 * IQR_abs)) | 
    (df_absolutos['valor'] > (Q3_abs + 1.5 * IQR_abs))
]

# Resultados
print(f"\n🔍 Outliers en Valores Absolutos ({len(outliers_abs)} registros):")
"""
print(outliers_abs[['nombre', 'valor', 'anio', 'fuente']].sort_values('valor', ascending=False))
"""
# Visualización
plt.figure(figsize=(10, 4))
sns.boxplot(data=df_absolutos, x='valor', color='skyblue')
plt.title("Distribución de Valores Absolutos (con Outliers)")
plt.show()

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

df_no_absolutos = df_unificado[df_unificado['nombre'].isin(indices)]


Q1_noabs = df_no_absolutos['valor'].quantile(0.25)
Q3_noabs = df_no_absolutos['valor'].quantile(0.75)
IQR_noabs = Q3_noabs - Q1_noabs

# Detección de outliers
outliers_noabs = df_no_absolutos[
    (df_no_absolutos['valor'] < (Q1_noabs - 1.5 * IQR_noabs)) | 
    (df_no_absolutos['valor'] > (Q3_noabs + 1.5 * IQR_noabs))
]


print(f"\n Outliers en Índices/Tasas ({len(outliers_noabs)} registros):")
"""
print(outliers_noabs[['nombre', 'valor', 'anio', 'fuente']].sort_values('valor', ascending=False))
"""

# Visualización
plt.figure(figsize=(10, 4))
sns.boxplot(data=df_no_absolutos, x='valor', color='salmon')
plt.title("Distribución de Índices/Tasas (con Outliers)")
plt.show()

# Año más reciente por fuente
actualizacion = df_unificado.groupby('fuente')['anio'].max()
print("\nAño más reciente por fuente:\n", actualizacion)

# Porcentaje de datos por período
df_unificado['decada'] = (df_unificado['anio'] // 10) * 10
print("\nDistribución por década:\n", df_unificado['decada'].value_counts().sort_index())

