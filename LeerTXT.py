from BarrioSustentable import *
import networkx as nx
import ast  # Necesario para evaluar strings que representan listas
import json
import re 
G = nx.Graph()


def read_nodes(file_path):
    G = nx.Graph()
    
    with open(file_path, 'r') as file:
        for line in file:
            # Limpiar espacios en blanco y saltos de línea
            line = line.strip()
            if not line:  # Saltarse líneas en blanco
                continue
            
            # Dividir la línea usando regex para manejar comas dentro de corchetes
            parts = re.split(r',\s*(?![^\[\]]*\])', line)
            if len(parts) < 9:
                print(f"Línea incompleta o mal formada: {line}")
                continue  # Saltar esta línea si no tiene todos los datos necesarios

            node_id = parts[0].strip()
            label = parts[1].strip().strip('"')
            Pe_inst = json.loads(parts[2].strip())
            Con_inst = json.loads(parts[3].strip())
            SOC = json.loads(parts[4].strip())
            SR = json.loads(parts[5].strip())
            X = float(parts[6].strip())
            Y = float(parts[7].strip())
            Techo_m2 = float(parts[8].strip())
            
            node_data = NodeData(label, Pe_inst, Con_inst, SOC, SR, X, Y, Techo_m2)
            G.add_node(node_id, data=node_data)
    
    return G

# Llamar a la función con la ruta correcta del archivo
#G = read_nodes('Casas.txt')
G = read_nodes('Casa2.txt')


def read_edges(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            source = parts[0].strip()
            target = parts[1].strip()
            weights = list(map(float, parts[2:]))  # Convertir textos a flotantes
            edge_data = EdgeData(*weights)
            G.add_edge(source, target, data=edge_data)

#read_edges('aristas.txt')
read_edges('Aristas2.txt')


"""
import matplotlib.pyplot as plt
for edge in G.edges(data=True):
    print(f"{edge[0]} -> {edge[1]}: {edge[2]['data']}")
    
# Grafico
pos = nx.spring_layout(G)  # Posicionamiento de los nodos
nx.draw(G, pos, with_labels=True, node_color='lightblue')  #Dibujo del grafo

# Etiquetas para las aristas
labels = {edge: G[edge[0]][edge[1]]['data'] for edge in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=6)  #Dibujo de etiquetas de las aristas 

plt.show() 

"""



