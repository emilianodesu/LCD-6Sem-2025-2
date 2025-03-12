import pandas as pd

df = pd.read_csv("./winequality-white.csv")
registros_completos = df.dropna().shape[0]  # Filas sin valores faltantes
registros_incompletos = len(df) - registros_completos  # Filas con al menos un valor faltante

# Calcular los porcentajes
porcentaje_completos = (registros_completos / len(df)) * 100
porcentaje_incompletos = (registros_incompletos / len(df)) * 100

# Mostrar los resultados
print(f"Porcentaje de registros completos: {porcentaje_completos: }%")
print(f"Porcentaje de registros incompletos: {porcentaje_incompletos: }%")