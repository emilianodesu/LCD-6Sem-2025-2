import pandas as pd

df = pd.read_csv('./winequality-white.csv')
porcentaje_duplicados = (df.duplicated().sum() / len(df)) * 100
print(f"Porcentaje de filas duplicadas: {porcentaje_duplicados: }%")