""" Sección 1 """

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

banco = pd.read_csv('./input/banco.csv')

# 1)
print(banco.describe(), end='\n\n')

# 2)
# Localiza y cuenta datos nulos en cada columna
print(banco.isnull().sum(), end='\n\n')

# 3)
marital_counts = banco['marital'].value_counts(normalize=True) * 100
plt.figure(figsize=(8, 8))
explode = (0.1, 0, 0)
plt.pie(marital_counts, labels=marital_counts.index,
        autopct='%1.1f%%', startangle=140, explode=explode)
plt.title('Porcentajes de Estados Civiles')
plt.show()

# 4)
filtro1 = banco[(banco['age'] > 50) & (banco['job'] == 'management')]
print(filtro1, end='\n\n')

# 5)
banco['loan'] = pd.get_dummies(banco['loan'], drop_first=True)
banco['loan'] = banco['loan'].astype(int)
print(banco.head(), end='\n\n')

# 6)
filtro2 = banco.loc[banco['education'] ==
                    'secondary', ['contact', 'housing', 'day']]
print(filtro2, end='\n\n')

# 7)
sns.boxplot(x=banco['balance'])
plt.title('Boxplot de Balance')
plt.show()
print(banco['balance'].describe(), end='\n\n')

# 8)
banco['risk'] = ((banco['housing'] == 'yes') & (
    banco['loan'] == 'yes') & (banco['contact'] == 'unknown')).astype(int)
print(banco, end='\n\n')

# 9)
plt.figure(figsize=(10, 6))
sns.scatterplot(x='age', y='balance', data=banco)
plt.title('Correlación Age vs Balance')
plt.xlabel('Age')
plt.ylabel('Balance')
plt.show()

# 10)
plt.figure(figsize=(12, 6))
sns.countplot(data=banco, x='job', order=banco['job'].value_counts().index)
plt.title('Distribución de Cuentahabientes por Trabajo')
plt.xlabel('Trabajo')
plt.ylabel('Cantidad')
plt.xticks(rotation=45)
plt.show()
