import pandas as pd
df=pd.read_csv('./winequality-white.csv')
faltante = (df.isnull().sum() / len(df)) * 100
print(faltante)