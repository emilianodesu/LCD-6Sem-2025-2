"""
===============================================================================
4. Utilizando la librearía json, transforma el grafo de networkx a una
representación en formato JSON
===============================================================================
"""
import json
import os

from Secc4In_1 import create_graph


class GraphToJson:
    def __init__(self, graph):
        """
        Inicializa el conversor con el grafo (por ejemplo, el devuelto por create_graph).
        """
        self.graph = graph

    def export_to_json(self, start_node, file_path):
        """
        Exporta el grafo a un archivo JSON, recorriéndolo mediante DFS a partir del nodo 'start_node'.

        Cada nodo se representa como un diccionario con:
          - "id": identificador del nodo.
          - "value": (opcional) contenido si el nodo es hoja.
          - "children": (opcional) lista de nodos hijos en la jerarquía.

        El JSON generado se escribe en el archivo ubicado en 'file_path'.
        """
        def dfs(node):
            node_dict = {"id": node}
            # Si el nodo posee el atributo "value", se agrega al diccionario.
            if "value" in self.graph.nodes[node]:
                node_dict["value"] = self.graph.nodes[node]["value"]
            # Recorrer recursivamente los hijos (sucesores) del nodo actual
            children = []
            for child in self.graph.successors(node):
                children.append(dfs(child))
            if children:
                node_dict["children"] = children
            return node_dict

        # Generar la representación del grafo en forma de diccionario
        graph_dict = dfs(start_node)
        # Convertir el diccionario a una cadena JSON con indentación para facilitar la lectura
        json_str = json.dumps(graph_dict, indent=4)
        # Escribir el contenido JSON en el archivo especificado
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json_str)


# Ejemplo de uso:
if __name__ == '__main__':
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

    # Crear el grafo y generar la representación JSON a partir del nodo "Company Projects"
    graph = create_graph()
    converter = GraphToJson(graph)
    converter.export_to_json(
        "Company Projects",
        os.path.join(BASE_PATH + '\\..\\output', "graph.json")
    )
