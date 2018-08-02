# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 18:17:07 2018

@author: andrew.mcdonald

This script will be used to create a synthetic log generator
The user specifies the earth model, top and bottom depths
"""

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

# Well Parameters
well_top_depth = 100
well_step = 0.5


# Earth Model
em_thickness = [30,10,20,30]


em_lith_list = ['shale', 'sandstone','sandstone', 'shale']
em_fluid_list = ['water', 'oil', 'water','water']

phit_lith = {'shale': 0.1, 'sandstone':0.25, 'limestone':0.10}
props_gr = {'shale': 120, 'sandstone':25, 'limestone':10}
props_mat_rhob = {'shale': 2.65, 'sandstone':2.65, 'limestone':2.71}
props_mat_dt = {'shale': 70, 'sandstone':55, 'limestone':47}
props_fluid_rho = {'oil': 0.8, 'gas':0.3, 'water':1.0}
props_fluid_dt = {'oil': 240, 'gas':900, 'water':189}

# Create a depth curve
well_bot_depth = (well_top_depth + sum(em_thickness)* well_step)

depth_count = well_top_depth
depth_list = []

while depth_count < well_bot_depth:
    depth_list.append(depth_count)
    depth_count += well_step


#Creating a thickness and lith list
interval_thickness=[]
lith_list =[]
fluid_list = []
matrix_rho = []

for thickness, lith, fluid in zip(em_thickness,em_lith_list,em_fluid_list):
    interval_thickness+= [thickness] * thickness
    lith_list+= [lith] * thickness
    fluid_list += [fluid] * thickness
    

# Build up synthetic gamma ray and porosity curves         
syn_gr = [props_gr[item] for item in lith_list]
syn_phit = [phit_lith[item] for item in lith_list]
syn_rho_fl = [props_fluid_rho[item] for item in fluid_list]
syn_rho_mat = [props_mat_rhob[item] for item in lith_list]
syn_dt_fl = [props_fluid_dt[item] for item in fluid_list]
syn_dt_mat = [props_mat_dt[item] for item in lith_list]

# build up synthetic RHOB and DT using the porosity input
#RHOB = (PHIT * RHOFL + (1 - PHIT) * RHOMatrix)
#DT =  (PHIT * DTFluid + (1 - PHIT) * DTMatrix)

syn_rhob = [(phi * fl + (1-phi) * mat) for (phi, fl, mat) in zip(syn_phit, syn_rho_fl, syn_rho_mat)]
syn_dt = [(phi * fl + (1-phi) * mat) for (phi, fl, mat) in zip(syn_phit, syn_dt_fl, syn_dt_mat)]


#syn_dt = []
#for lith, porosity, in zip(lith_list,syn_phit):
#    syn_rhob.append(porosity * 1 + (1-porosity) * 2.65)
#    syn_dt.append(porosity * 190 + (1-porosity) * 55)
    

    

# Build up a synthetic NPHI curve



# Add a small amount of noise to the logs
noise = [(random.randint(0,100)/10) for item in lith_list]
noise_inv = [(item * -1) for item in noise]
syn_gr_noised = [sum(x) for x in zip(syn_gr, noise)]
syn_dt_noised = [sum(x) for x in zip(syn_dt, noise)]




#Creation of our main data frame

dataset = pd.DataFrame({'DEPTH':np.arange(well_top_depth,well_bot_depth,well_step)})
dataset = pd.DataFrame({'GR':np.arange(well_top_depth,well_bot_depth,well_step)})


# Plot data on a log plot along side scatter plots (5 vertical tracks ??)

fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, sharey=True)

ax1.plot(syn_gr_noised, depth_list)
ax1.set_xlim(0,150)
ax1.invert_yaxis()
ax1.set_xlabel('Gamma')
ax1.xaxis.set_label_position('top')

ax2.plot(syn_rhob, depth_list)
ax2.set_xlim(1.95,2.95)
ax2.set_xlabel('Density')

ax3.plot(syn_dt_noised, depth_list)
ax3.set_xlim(140,40)
ax3.set_xlabel('DT Compr.')

plt.tight_layout()

plt.show()