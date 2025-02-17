"""
===============================================================================
3. Utilizando el modulo xml.etree.ElementTree, transforma el grafo de networkx
a una representación XML
===============================================================================
"""

import xml.etree.ElementTree as ET
from collections import deque
import os

from Secc4In_1 import create_graph


class GraphXMLConverter:
    def __init__(self, graph):
        """
        Inicializa el convertidor con el grafo proporcionado.
        """
        self.graph = graph

    def export_to_xml(self, start_node, file_path):
        """
        Exporta el grafo a un archivo XML, recorriéndolo en anchura (BFS) a partir del nodo 'start_node'.
        Cada nodo se representa con una etiqueta <nodo> que contiene un atributo 'id' con el identificador del nodo.
        Si un nodo es hoja (posee el atributo 'value'), su valor se asigna como contenido textual de la etiqueta.
        El archivo XML se genera en la ruta especificada por 'file_path'.
        """
        # Crear el elemento raíz "nodo" y asignar el atributo id con el identificador del nodo de inicio.
        root = ET.Element("nodo")
        root.set("id", start_node)
        if "value" in self.graph.nodes[start_node]:
            root.text = str(self.graph.nodes[start_node]["value"])

        # Utilizar una cola para realizar la búsqueda BFS: cada elemento es una tupla (identificador del nodo, elemento XML)
        queue = deque()
        queue.append((start_node, root))

        while queue:
            current_node, current_elem = queue.popleft()
            for child in self.graph.successors(current_node):
                # Crear el elemento para el hijo con etiqueta "nodo" y asignar su identificador al atributo "id"
                child_elem = ET.Element("nodo")
                child_elem.set("id", child)
                if "value" in self.graph.nodes[child]:
                    child_elem.text = str(self.graph.nodes[child]["value"])
                # Anexar el elemento hijo al nodo actual para mantener la jerarquía
                current_elem.append(child_elem)
                queue.append((child, child_elem))

        # Crear el árbol XML y escribirlo en la ruta especificada
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='unicode', xml_declaration=True)


if __name__ == '__main__':
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

    # Crear el grafo y convertirlo a XML a partir del nodo "Company Projects"
    graph = create_graph()
    converter = GraphXMLConverter(graph)
    converter.export_to_xml(
        "Company Projects",
        os.path.join(BASE_PATH + '\\..\\output', "company_projects.xml"))
