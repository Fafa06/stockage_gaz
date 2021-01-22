#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 12:07:00 2020

@author: guillaumefalandry
"""

from gurobipy import *
import numpy as np
import pandas as pd
from random import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


Vmax=25000
inj_nominale=299.117
sout_nominale=568.12
prix_gaz=13
durée=365
prix=13
cout_fixe=259999


#paramètres d'injection
stock_inj=np.array([0,0.6,1])
facteur_reduction_inj=np.array([1,1,0.43])
inj=inj_nominale*facteur_reduction_inj



#paramètres de soutirage
stock_sout=np.array([0,0.3,0.8,1])
facteur_reduction_sout=np.array([0.7,0,0.95,1])
sout=sout_nominale*facteur_reduction_sout



stockage=Model('Stockage Gaz')
#variable décisionnelles
stock=stockage.addVars(365,lb=0,ub=inj_nominale,vtype=GRB.CONTINUOUS)
decison=stockage.addVars(365,lb=-1,ub=1,vtype=GRB.INTEGER)


#variables de modélisation de la fonction linéaire
lambda_inj=stockage.addVars(3,365,vtype=GRB.CONTINUOUS,ub=1)
for i in range(365):
    stockage.addSOS(GRB.SOS_TYPE2,[lambda_inj[j,i] for j in range(3)])

lambda_sout=stockage.addVars(4,365,vtype=GRB.CONTINUOUS,ub=1)
for i in range(365):
    stockage.addSOS(GRB.SOS_TYPE2,[lambda_sout[j,i] for j in range(4)])

# Contraintes de Tunnel

stockage.addConstr(stock[62]<=16250)
stockage.addConstr(stock[62]>=5000)
stockage.addConstr(stock[123]<=22500)
stockage.addConstr(stock[123]>=12500)
stockage.addConstr(stock[154]<=23750)
stockage.addConstr(stock[154]>=21250)

for i in range(durée):
    
    stock[i]=stock[i-1]+decision[i]*inj[i]-
    
    # Contraintes du débit d'injection
    stockage.addConstr(quicksum(lambda_inj[j,i] for j in range(3))==1)
    stockage.addConstr(quicksum(Vmax*stock_inj[j]*lambda_inj[j,i])==stock[i])
    stockage.addConstr(quicksum(facteur_reduction_inj[j]*lambda_inj[j,i])==inj[i])
    
    # Contraintes du débit de soutirage
    stockage.addConstr(quicksum(lambda_sout[j,i] for j in range(4))==1)
    stockage.addConstr(quicksum(Vmax*stock_sout[j]*lambda_soutj[j,i])==stock[i])
    stockage.addConstr(quicksum(facteur_reduction_sout[j]*lambda_sout[j,i])==sout[i])



    




