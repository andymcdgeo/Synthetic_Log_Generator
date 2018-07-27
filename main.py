# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 18:17:07 2018

@author: andrew.mcdonald

This script will be used to create a synthetic log generator
The user specifies the earth model, top and bottom depths
"""

import numpy as np
import pandas as pd

# Well Parameters
well_top_depth = 0
well_interval = 100
well_step = 0.5
well_bot_depth = well_top_depth + well_interval

# Earth Model
# Number of layers
em_layers = 2

#Layer thickness in depth units
em_layer_1 = 20
em_layer_2 = 70
em_layer_3 = 10

em_list = [em_layer_1, em_layer_2, em_layer_3]

gr=[]


index = well_top_depth
while index < well_bot_depth:
    for value in em_list:
        #gr = sum(([n]*n for n in em_list),[])
        gr+= [value] * value
    index += well_step

#Creation of our main data frame
 
dataset = pd.DataFrame({'DEPTH':np.arange(well_top_depth,well_bot_depth,well_step)})
dataset = pd.DataFrame({'GR':np.arange(well_top_depth,well_bot_depth,well_step)})


#
#def curve_create_depth(well_top_depth,well_bot_depth,well_step):
#    return pd.DataFrame({'DEPTH':np.arange(well_top_depth,well_bot_depth,well_step)})




    
