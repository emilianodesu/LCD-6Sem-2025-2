# #### Sección 3
# 
# 1. Utiliza networkx para generar la gráfica de la Figura 1.
# 
# ![Figura 1](img/Fig1.png)
# 
# 2. Genera e imprime en pantalla la matriz de adyacencias de esta gráfica.
# 3. Imprime el grado de cada vértice.

# In[3]:


import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from(range(1, 10))
edges = [(5, 3), (3, 4), (3, 2), (8, 4), (4, 9), (2, 1), (1, 6), (2, 6), (6, 7), (4, 2)]
G.add_edges_from(edges)

nx.draw_networkx(G)
ax = plt.gca()
ax.margins(0.20)
plt.axis('off')
plt.show()

adj_matrix = nx.adjacency_matrix(G)
print('Matriz de adyacencias\n', adj_matrix.todense(), end='\n\n')

degrees = dict(G.degree())
print('Grado de los vertices\n', degrees)


