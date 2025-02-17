"""
===============================================================================
2. Visualiza el grafo utilizando la librería matplotlib.pyplot
===============================================================================
"""
import matplotlib.pyplot as plt
import networkx as nx
from pprint import pformat

from Secc4In_1 import create_graph


def draw_graph():
    G = create_graph()
    pos = nx.shell_layout(G)
    labels = {
        node: f"{node}\n{pformat(data)}"
        for node, data in G.nodes(data=True)
    }
    pos = nx.spring_layout(G)
    _, ax = plt.subplots(figsize=(15, 10))
    nx.draw_networkx_nodes(G, pos, node_size=5000, node_color='skyblue', ax=ax)
    nx.draw_networkx_edges(G, pos, ax=ax)
    nx.draw_networkx_labels(G, pos, labels, font_size=10,
                            font_weight='bold', ax=ax)
    plt.title("Representación gráfica Esquemas")
    plt.axis("off")
    plt.show()


def main():
    draw_graph()


if __name__ == "__main__":
    main()
