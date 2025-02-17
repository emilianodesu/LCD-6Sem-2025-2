"""
===============================================================================
5. Visualiza el grafo lo mas parecido al grafo proporcionado al inicio
===============================================================================
"""
import networkx as nx
import matplotlib.pyplot as plt


def create_graph():
    """
    Crea y devuelve un grafo dirigido con los nodos y aristas harcodeados.
    """
    G = nx.DiGraph()
    G.add_node("Company projects")
    edges = [
        ("Company projects", "Project 1"),
        ("Company projects", "Project 2"),
        ("Project 1", "Name"),
        ("Project 1", "Number"),
        ("Project 1", "Location"),
        ("Project 1", "Worker 1"),
        ("Project 1", "Worker 2"),
        ("Worker 1", "Ssn1"),
        ("Worker 1", "Last_name"),
        ("Worker 1", "Hours1"),
        ("Worker 2", "Ssn2"),
        ("Worker 2", "First_name"),
        ("Worker 2", "Hours2"),
    ]
    G.add_edges_from(edges)
    return G


def get_positions():
    """
    Define las posiciones de cada nodo en el grafo
    """
    pos = {
        'Company projects': (0, 0),
        'Project 1': (-3, -1),
        'Project 2': (3, -1),
        'Name': (-5, -2),
        'Number': (-4, -2),
        'Location': (-3, -2),
        'Worker 1': (-2, -2),
        'Worker 2': (1, -2),
        'Ssn1': (-3, -3),
        'Last_name': (-2, -3),
        'Hours1': (-1, -3),
        'Ssn2': (0, -3),
        'First_name': (1, -3),
        'Hours2': (2, -3),
    }
    return pos


def get_label_positions(pos):
    """
    A partir de las posiciones originales de los nodos, se definen posiciones personalizadas
    para las etiquetas, ajustando la posición de algunos nodos.
    """
    label_pos = {k: (v[0], v[1]) for k, v in pos.items()}
    custom_positions = {
        'Company projects': (0, 0.12),
        'Project 1': (-3, -0.8),
        'Project 2': (3, -0.8),
        'Worker 1': (-2.5, -1.8),
        'Worker 2': (1, -1.8),
        'Name': (-5, -1.8),
        'Number': (-4.2, -1.8),
        'Location': (-3.35, -1.8),
        'Ssn1': (-3.1, -2.8),
        'Last_name': (-2.3, -2.8),
        'Hours1': (-1.5, -2.8),
        'Ssn2': (0, -2.8),
        'First_name': (0.6, -2.8),
        'Hours2': (1.5, -2.8),
    }
    label_pos.update(custom_positions)
    return label_pos


def draw_graph(G, pos, label_pos):
    """
    Dibuja el grafo y sus etiquetas utilizando las posiciones especificadas.
    """
    nx.draw(
        G, pos=pos,
        with_labels=False,
        node_size=400,
        node_color='black',
        alpha=0.8,
        arrowsize=40,
        width=3
    )
    nx.draw_networkx_labels(G, pos=label_pos, font_size=15)


def add_text_annotations(texts):
    """
    Añade anotaciones de texto al plot. 'texts' es una lista de diccionarios
    donde cada uno contiene las claves 'x', 'y' y 'text', además de opcionalmente 'fontdict'.
    """
    defaultFontDict = {'size': 15, 'color': 'black'}
    for item in texts:
        plt.text(
            item["x"],
            item["y"],
            item["text"],
            fontdict=item.get("fontdict", defaultFontDict)
        )


def draw_arrows(arrows):
    """
    Dibuja flechas en el plot a partir de una lista de diccionarios que contienen
    los parámetros necesarios para plt.arrow.
    """
    for params in arrows:
        plt.arrow(**params)


def main():
    G = create_graph()
    pos = get_positions()
    label_pos = get_label_positions(pos)
    plt.figure(figsize=(20, 10))
    draw_graph(G, pos, label_pos)
    text_annotations = [
        {"x": -5.2, "y": -2.15, "text": '"Product X"'},
        {"x": -4,   "y": -2.15, "text": '1'},
        {"x": -3.2, "y": -2.15, "text": '"Bellaire"'},
        {"x": -3.4, "y": -3.15, "text": '"123456789"'},
        {"x": -2.25, "y": -3.15, "text": '"Smith"'},
        {"x": -1.1, "y": -3.15, "text": '32.5'},
        {"x": -0.3, "y": -3.15, "text": '"435435435"'},
        {"x": 0.8,  "y": -3.15, "text": '"Joyce"'},
        {"x": 2,    "y": -3.15, "text": '20.0'},
    ]
    add_text_annotations(text_annotations)
    arrow_params_list = [
        {
            "x": 3,
            "y": -1,
            "dx": -1.5,
            "dy": -0.8,
            "head_width": 0.1,
            "head_length": 0.1,
            "fc": 'black',
            "ec": 'black'
        },
        {
            "x": 3,
            "y": -1,
            "dx": 1.5,
            "dy": -0.8,
            "head_width": 0.1,
            "head_length": 0.1,
            "fc": 'black',
            "ec": 'black'
        },
    ]
    draw_arrows(arrow_params_list)
    plt.show()

main()
