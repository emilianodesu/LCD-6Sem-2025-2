"""
===============================================================================
1. Representa este grafo utilizando la librería NetworkX de python.
===============================================================================
"""


import networkx as nx


def create_graph():
    """
    Crea y devuelve un grafo dirigido con los nodos y aristas harcodeados
    'nodes'.
    """
    nodes = {
        "name": "Company Projects",
        "children": [
            {
                "name": "Project 1",
                "children": [
                    {
                        "name": "Name",
                        "value": "Product X"
                    },
                    {
                        "name": "Number",
                        "value": 123
                    },
                    {
                        "name": "Location",
                        "value": "Bellaire"
                    },
                    {
                        "name": "Worker 1",
                        "children": [
                            {
                                "name": "ssn_1",
                                "value": 123456789
                            },
                            {
                                "name": "first_name_1",
                                "value": "Smith"
                            },
                            {
                                "name": "hours_1",
                                "value": 40.00
                            }
                        ]
                    },
                    {
                        "name": "Worker 2",
                        "children": [
                            {
                                "name": "ssn_2",
                                "value": 987654321
                            },
                            {
                                "name": "first_name_2",
                                "value": "Joyce"
                            },
                            {
                                "name": "hours_2",
                                "value": 40.00
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Project 2"
            }
        ],
    }
    G = nx.DiGraph()

    def add_nodes_recursive(data, parent_id=None):
        # Usar el atributo "name" como identificador único del nodo
        node_id = data["name"]
        attr = {}
        if "value" in data:
            attr["value"] = data["value"]
        G.add_node(node_id, **attr)
        if parent_id is not None:
            G.add_edge(parent_id, node_id)
        for child in data.get("children", []):
            add_nodes_recursive(child, parent_id=node_id)

    add_nodes_recursive(nodes)
    return G


if __name__ == "__main__":
    print("".join(['\n' for _ in range(3)]))
    G = create_graph()
    print("Nodes:")
    for node in G.nodes:
        print(f" - {node}")
    print("\nEdges:")
    for edge in G.edges:
        print(f" - {edge[0]} -> {edge[1]}")
