# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:51:40 2024

@author: conim
"""

class NodeData:
    def __init__(self, label, Pe_inst=None, Con_inst=None, SOC=None, SR=None, X=None, Y=None, Techo_m2=None):
        self.label = label  #Etiqueta del nodo
        self.Pe_inst = Pe_inst if Pe_inst is not None else []  #Lista de potencia instalada generada
        self.Con_inst = Con_inst if Con_inst is not None else []  #Lista de consumo instalado (1 dato por hora)
        self.SOC = SOC if SOC is not None else []  #Lista de estado de carga
        self.SR = SR if SR is not None else []  #Lista de estados booleanos
        self.X = X
        self.Y = Y
        self.Techo_m2 = Techo_m2

    def __repr__(self):
        return f"NodeData(Etiqueta='{self.label}', Pe_inst={self.Pe_inst}, Con_inst={self.Con_inst}, SOC={self.SOC}, SR={self.SR},Coordenada X={self.X},Coordenada Y={self.Y}, metro cuadrado de techo libre={Techo_m2})"

class EdgeData:
    def __init__(self, Pe, Pc, Z, D, R, C):
        self.Pe = Pe  #Potencia entrante
        self.Pc = Pc  #Potencia consumida
        self.Z = Z    #Impedancia
        self.D = D    #Distancia
        self.R = R    #Resistencia
        self.C = C    #Condición booleana

    def __repr__(self):
        return f"EdgeData(Pe={self.Pe}, Pc={self.Pc}, Z={self.Z}, D={self.D}, R={self.R}, C={self.C})"
    
