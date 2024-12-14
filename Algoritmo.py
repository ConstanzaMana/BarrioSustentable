# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 17:58:39 2024

@author: conim
"""
#probar de normalizar
#ver de poner todas las restricciones en inicializar y despues en la funcion de calcular no 
import numpy as np
import random
import networkx as nx
import re
import json
from LeerTXT import *

NUM_CASAS = 13
MAX_PANELES_SOLARES = 100
consumo_Electrodomesticos = [1048, 200, 5, 90, 113, 1225, 640, 2000, 100, 22, 1125, 800, 950]
capacidad_panel_solar = 2  # kWh/día por panel
dimension_paneles = 1 * 1.6

def calcular_perdida_energia(solucion, grafo, consumo_Electrodomesticos, capacidad_panel_solar):
    perdida_total = 0
    ubicaciones_casas = {node_id: casa for node_id, casa in grafo.nodes.data('data')}
    ubicacion_generador = solucion['ubicacion_generador']
    paneles_por_casa = solucion['paneles_por_casa']

    for casa_label, casa in ubicaciones_casas.items():
        casa_index = int(casa_label.split()[0].replace('Nodo', '')) - 1
        if 0 <= casa_index < len(paneles_por_casa):
            paneles_instalados = paneles_por_casa[casa_index]
            techo = float(casa.Techo_m2) if casa.Techo_m2 is not None else 0
            max_paneles_permitidos = techo // dimension_paneles
            if paneles_instalados > max_paneles_permitidos:
                paneles_instalados = max_paneles_permitidos
                paneles_por_casa[casa_index] = paneles_instalados

        xc = float(casa.X)
        yc = float(casa.Y)
        consumo_total = sum(consumo_Electrodomesticos[i] * casa.Con_inst[i] for i in range(len(consumo_Electrodomesticos)))
        xg = float(ubicacion_generador[0])
        yg = float(ubicacion_generador[1])
        distancia = np.sqrt((xc - xg) ** 2 + (yc - yg) ** 2)
        generacion_potencial = capacidad_panel_solar * paneles_instalados
        perdida_total += distancia * (consumo_total - generacion_potencial)
        
        margen_proximidad = 0.9
        # Penalización por proximidad al generador
        if abs(xg - xc) <= margen_proximidad and abs(yg - yc) <= margen_proximidad:
            perdida_total += 100000
   
            
    #print(f"{sum(paneles_por_casa)}")
    return perdida_total

def inicializar_poblacion(num_individuos, grafo):
    #Inicializo las coordenadas de la estacion teniendo en cuenta que este dentro del 
    #area de las casas
    ubicaciones_casas = {node_id: casa for node_id, casa in grafo.nodes.data('data')}
    min_x = min(casa.X for casa in ubicaciones_casas.values())
    max_x = max(casa.X for casa in ubicaciones_casas.values())
    min_y = min(casa.Y for casa in ubicaciones_casas.values())
    max_y = max(casa.Y for casa in ubicaciones_casas.values())
    poblacion = []
    
    while len(poblacion) < num_individuos:
        paneles_por_casa = []
        #Creo una lista con la cantidad de paneles_por_casa
        for casa_label, casa in ubicaciones_casas.items():
            casa_index = int(casa_label.split()[0].replace('Nodo', '')) - 1
            techo_disponible = int(float(casa.Techo_m2) // dimension_paneles)
            consumo = consumo_Electrodomesticos[casa_index] // capacidad_panel_solar
            #Cantidad de paneles teniendo en cuenta el area del techo y que no exceda el consumo de la casa
            max_paneles_asignados = min(techo_disponible, consumo)
            paneles_asignados = random.randint(0, max_paneles_asignados)
            paneles_por_casa.append(paneles_asignados)
        
        solucion = {
            'ubicacion_generador': (random.uniform(min_x, max_x), random.uniform(min_y, max_y)),
            'paneles_por_casa': paneles_por_casa
        }
        #Verifico si el individuo creado verifica las restricciones y lo sumo a la poblacion
        if verificar_restricciones(solucion, grafo):
            poblacion.append(solucion)
    
    return poblacion


def verificar_restricciones(solucion, grafo):
    ubicaciones_casas = {node_id: casa for node_id, casa in grafo.nodes.data('data')}
    paneles_por_casa = solucion['paneles_por_casa']
    
    # Verificar la restricción de cantidad máxima de paneles solares por casa
    for i, (casa_label, casa) in enumerate(ubicaciones_casas.items()):
        techo_disponible = int(float(casa.Techo_m2) // dimension_paneles)
        consumo = consumo_Electrodomesticos[i] // capacidad_panel_solar
        max_paneles_asignados = min(techo_disponible, consumo)
        
        if paneles_por_casa[i] > max_paneles_asignados:
            return False
    
    # Verificar la restricción de cantidad máxima total de paneles solares
    if sum(paneles_por_casa) > MAX_PANELES_SOLARES:
        return False
    
    return True


def evaluar_poblacion(poblacion, grafo, consumo_Electrodomesticos, capacidad_panel_solar):
    evaluaciones = []
    for solucion in poblacion:
        if verificar_restricciones(solucion, grafo):
            perdida_energia = calcular_perdida_energia(solucion, grafo, consumo_Electrodomesticos, capacidad_panel_solar)
            evaluaciones.append((solucion, perdida_energia))
    evaluaciones.sort(key=lambda x: x[1])  # Ordenar por pérdida de energía (menor es mejor)
    
    # Asegurarse de que hay suficientes soluciones válidas
    if len(evaluaciones) < NUM_PADRES:
        print("Advertencia: No hay suficientes soluciones válidas.")
        while len(evaluaciones) < NUM_PADRES:
            evaluaciones.append((poblacion[random.randint(0, len(poblacion)-1)], float('inf')))
    return evaluaciones


#selección por clasificación, en funcion de la evaluacion
#selecciono los primeros  de la lista ordenada por pérdida de energía ascendente
def seleccionar_padres(evaluaciones, num_padres):
    padres = []
    for i in range(num_padres):
        padres.append(evaluaciones[i][0])
    return padres

def cruzar(padre1, padre2, grafo):
    ubicaciones_casas = {node_id: casa for node_id, casa in grafo.nodes.data('data')}
    min_x = min(casa.X for casa in ubicaciones_casas.values())
    max_x = max(casa.X for casa in ubicaciones_casas.values())
    min_y = min(casa.Y for casa in ubicaciones_casas.values())
    max_y = max(casa.Y for casa in ubicaciones_casas.values())

    ubicacion_generador_hijo = (
        random.uniform(min(padre1['ubicacion_generador'][0], padre2['ubicacion_generador'][0]),
                       max(padre1['ubicacion_generador'][0], padre2['ubicacion_generador'][0])),
        random.uniform(min(padre1['ubicacion_generador'][1], padre2['ubicacion_generador'][1]),
                       max(padre1['ubicacion_generador'][1], padre2['ubicacion_generador'][1]))
    )

    paneles_por_casa_hijo = []
    for i, (pan1, pan2) in enumerate(zip(padre1['paneles_por_casa'], padre2['paneles_por_casa'])):
        if random.random() < 0.5:
            paneles_hijo = pan1
        else:
            paneles_hijo = pan2

        # Verificar y ajustar los paneles por casa según el techo disponible
        casa_label = f'Nodo{i+1}'
        casa = ubicaciones_casas[casa_label]
        techo_disponible = int(float(casa.Techo_m2) // dimension_paneles)
        consumo = consumo_Electrodomesticos[i] // capacidad_panel_solar
        max_paneles_asignados = min(techo_disponible, consumo)
        if paneles_hijo > max_paneles_asignados:
            paneles_hijo = max_paneles_asignados

        paneles_por_casa_hijo.append(paneles_hijo)

    # Verificar la cantidad total de paneles y ajustar si es necesario
    total_paneles = sum(paneles_por_casa_hijo)
    if total_paneles > MAX_PANELES_SOLARES:
        factor_ajuste = MAX_PANELES_SOLARES / total_paneles
        paneles_por_casa_hijo = [int(paneles * factor_ajuste) for paneles in paneles_por_casa_hijo]

    return {'ubicacion_generador': ubicacion_generador_hijo, 'paneles_por_casa': paneles_por_casa_hijo}

def mutar(solucion, grafo):
    ubicaciones_casas = {node_id: casa for node_id, casa in grafo.nodes.data('data')}
    min_x = min(casa.X for casa in ubicaciones_casas.values())
    max_x = max(casa.X for casa in ubicaciones_casas.values())
    min_y = min(casa.Y for casa in ubicaciones_casas.values())
    max_y = max(casa.Y for casa in ubicaciones_casas.values())

    for i in range(NUM_CASAS):
        if random.random() < 0.1:
            solucion['ubicacion_generador'] = (random.uniform(min_x, max_x), random.uniform(min_y, max_y))
            casa = ubicaciones_casas[f'Nodo{i+1}']
            techo_disponible = int(float(casa.Techo_m2) // dimension_paneles)
            consumo = consumo_Electrodomesticos[i] // capacidad_panel_solar
            max_paneles_asignados = min(techo_disponible, consumo)
            solucion['paneles_por_casa'][i] = random.randint(0, max_paneles_asignados)
    
    return solucion

NUM_GENERACIONES = 1000
NUM_INDIVIDUOS = 100
NUM_PADRES = 10

poblacion = inicializar_poblacion(NUM_INDIVIDUOS, G)

for generacion in range(NUM_GENERACIONES):
    evaluaciones = evaluar_poblacion(poblacion, G, consumo_Electrodomesticos, capacidad_panel_solar)
    padres = seleccionar_padres(evaluaciones, NUM_PADRES)
    nueva_poblacion = []
    for _ in range(NUM_INDIVIDUOS):
        padre1 = random.choice(padres)
        padre2 = random.choice(padres)
        hijo = cruzar(padre1, padre2, G)
        hijo = mutar(hijo, G)
        nueva_poblacion.append(hijo)
    poblacion = nueva_poblacion

mejor_solucion, mejor_perdida_energia = evaluar_poblacion(poblacion, G, consumo_Electrodomesticos, capacidad_panel_solar)[0]

print(f"Mejor pérdida de energía encontrada: {mejor_perdida_energia}")
print(f"Ubicación del generador óptimo: {mejor_solucion['ubicacion_generador']}")
print(f"Paneles por casa en la mejor solución: {mejor_solucion['paneles_por_casa']}")
print(f"Total de paneles en la mejor solución: {sum(mejor_solucion['paneles_por_casa'])}")


import matplotlib.pyplot as plt
# Posiciones de los nodos
pos = {node_id: (casa.X, casa.Y) for node_id, casa in G.nodes.data('data')}
# Etiquetas de los nodos con la cantidad de paneles
labels = {node_id: f"{node_id}\n{paneles}" for node_id, paneles in zip(G.nodes, mejor_solucion['paneles_por_casa'])}
plt.figure(figsize=(10, 10))
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
#Etiquetas de los nodos
nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
#ubicación del generador
plt.scatter(mejor_solucion['ubicacion_generador'][0], mejor_solucion['ubicacion_generador'][1], color='red', s=200, label='Generador')
plt.legend()
plt.title('Distribución de Paneles Solares y Generador')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.grid()
plt.show()

#Algoritmo genetico - Objetivos
#Ubicar los generadores de manera óptima para minimizar las pérdidas debido a la distancia.
#Distribuir los paneles solares de manera óptima entre las casas para maximizar la eficiencia de generación y cubrir el consumo.

#individuo
# Vector con las primeras posiciones para las coordenas XY de cada generador
# la segunda parte del vector son los numeros de paneles asignados a cada casa 

#Función de aptitud
#Minimización de las pérdidas: Distancia entre las casas y los generadores.
#Cobertura del consumo: Asegurarte de que el consumo de cada casa está cubierto por la generación total (incluyendo sus propios paneles solares).

#Centroide de las ubicaciones casas: (37.12794999999999, -122.45884999999998)
