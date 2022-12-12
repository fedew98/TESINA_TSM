#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

class usuario:
    
    def __init__(self,tipo,alpha, start_joining):
        self.tipo = tipo
        self.alpha = alpha
        self.join = start_joining
        
        self.join_bu = start_joining
        
    def U(self,DC,P):
        return self.alpha*DC-P
    
    def update_choice(self,DC,P):
        self.join = self.U(DC,P) >= 0   
        
    def restore_choice(self):
        
        self.join = self.join_bu
        

class plataforma:
    
    def __init__(self, starting_PA,starting_PB,FA,FB):
        self.PA, self.PB = starting_PA,starting_PB
        self.FA, self.FB = FA,FB
        
    def profit(self, DA, DB):
        return DA*(self.PA-self.FA)+DB*(self.PB-self.FB)
    
    def update_price(self,PA,PB):
        self.PA, self.PB = PA,PB


def update_prices(A,B,PA,PB,Da,Db):
    
    for a in A:
        a.update_choice(Db,PA)

    for b in B:
        b.update_choice(Da,PB)

def update_prices_to_eq(I,A,B,PA,PB, print_result = False,graph=False, IT_max = 50):
    it = 0
    Da = -2
    Db = -2
    Da_temp = -1
    Db_temp = -1
    hist = []
    if print_result:
        print('It','Da','Db')
    I.update_price(PA,PB)    
    for it in range(IT_max):
        Da = np.sum([a.join for a in A])
        Db = np.sum([b.join for b in B])
        
        update_prices(A,B,PA,PB,Da,Db)
        Da_temp = np.sum([a.join for a in A])
        Db_temp = np.sum([b.join for b in B])
        
        if print_result:
            print(it,Da,Db)
            
        hist.append([Da,Db,I.profit(Da,Db)])
        
        if (((Da == Da_temp) & (Db == Db_temp))):
            break
    
  
    if it == IT_max:
        print(F"Error en {PA};{PB}")
        
    for t in range(5):
        hist.append([Da,Db,I.profit(Da,Db)])
    
    hist = pd.DataFrame(hist,columns=['Da','Db','Beneficio_I'])
    if graph:
        return hist,it

def update_prices_to_max(A,B,I, PA_R,PB_R, graph=True, IT_max = 50):
    hist = []
    for pa in PA_R:
        for pb in PB_R:
                      
            for a in A:
                a.restore_choice()
            for b in B:
                b.restore_choice()
            
            update_prices_to_eq(I,A,B,pa,pb,False,False,IT_max)
            Da = np.sum([a.join for a in A])
            Db = np.sum([b.join for b in B])
            Pi = I.profit(Da,Db)
            hist.append([pa,pb,Da,Db,Pi])
            
    hist = pd.DataFrame(data=hist, columns = ["PA","PB","DA","DB","BENEFICIO"])
    
    if graph:
        fig, ax = plt.subplots(1,2,figsize=(18,6))
        
        max_point = hist[hist.BENEFICIO == hist.BENEFICIO.max()]


        hist.plot.scatter(ax = ax[0], x='PA', y='PB', c= 'BENEFICIO',cmap='OrRd')
        hist.plot.scatter(ax = ax[1], x='DA', y='DB', c= 'BENEFICIO',cmap='OrRd')



        for r in max_point.index:
            ax[0].text(max_point.loc[r,'PA'],max_point.loc[r,'PB'],'MAX: ('+str(max_point.loc[r,'PA'])+';'+str(max_point.loc[r,'PB'])+')',color='blue', weight='bold')

        for r in max_point.index:
            ax[1].text(max_point.loc[r,'DA'],max_point.loc[r,'DB'],'MAX: ('+str(max_point.loc[r,'DA'])+';'+str(max_point.loc[r,'DB'])+')',color='blue', weight='bold')
    return hist
    

