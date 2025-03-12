'''Uso de la librería missingno para visualizar valores faltantes en un dataset'''
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt


# Cargar el dataset
df = pd.read_csv("heart_disease_uci.csv")

# Visualizar valores faltantes
msno.bar(df)
plt.show()
