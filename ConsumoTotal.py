from LeerTXT import *

consumo_Electrodomesticos = [1048, 200, 5, 90, 113, 1225, 640, 2000, 100, 22, 1125, 800, 950]

def calcular_consumo_total(casa, consumo_vector):
    #Le podria agregue el *8 (horas)
    total_consumo = sum(casa.Con_inst[i] * consumo_Electrodomesticos[i] for i in range(len(consumo_Electrodomesticos)))
    return total_consumo

# Calcular el consumo total para cada casa
for node_id, data in G.nodes(data=True):
    casa = data['data']
    total = calcular_consumo_total(casa, consumo_Electrodomesticos)
    print(f"Consumo total de {casa.label}: {total}")
    
    
#Un panel solar producirá un promedio de unos 2 kilovatios hora (kWh) de electricidad diaria.
#La mayoría de viviendas instalan 15 paneles solares, lo que genera un promedio de 30kWh de energía solar diaria.
# 1 metro de ancho por 1.6 metros de largo
#Voy a tener disponibles 100 paneles para distribuir

#Tambien estan las estaciones con ubicacion (en principio) variable

"""
Consumo total de Casa 1: 8714
Consumo total de Casa 2: 10348 --
Consumo total de Casa 3: 6185
Consumo total de Casa 4: 4554
Consumo total de Casa 5: 10989 --
Consumo total de Casa 6: 7425
Consumo total de Casa 7: 6091
Consumo total de Casa 8: 9225 --
Consumo total de Casa 9: 11563 --
Consumo total de Casa 10: 8020
"""