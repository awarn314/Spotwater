# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 22:38:55 2018

@author: Alex
"""

#import packages
import pandas as pd
import numpy as np
from bokeh.io import curdoc

# Each tab is drawn by one script
from PlotTabs.heatmap import heatmap_tab
from PlotTabs.bar import bar_tab
from PlotTabs.single_pie import single_pie_tab
from PlotTabs.radar import radar_tab
from PlotTabs.radar_norm import radar_norm_tab
from PlotTabs.rings import rings_tab
from PlotTabs.intervals import intervals_tab
from bokeh.models.widgets import Select, Panel, Tabs, CheckboxGroup
from Funcs.Functions import Mean_Groupings, cmpd_options_func, circ,clean_df,Put_Cmpds_Into_Grps
import os

os.system('cd /D C:\ folder_location_goes_here')
os.system("bokeh serve --show Spotwater.py")

#####Inputs go here####
data_fn='Large data set.xlsx' #experimental data
number_cmpds_run=52 #how many compounds did you run
replicate=[]
Time=['Time'] #name of time column
Treatments=['Treatment 1', 'Treatment 2', 'Treatment 3'] #these must match your column titles


master_fn='Master-Sheet.xlsx' #master data sheet of groups vs compounds
Groups=['Alcohol','Amine','Esters','Ethers','Ketones','Acids']



######## Program is below here#############
df = clean_df(data_fn,replicate,Treatments)
Cmpd_Groupings=Put_Cmpds_Into_Grps(master_fn,Groups)
df_means, df_stdev = Mean_Groupings(df,number_cmpds_run,Time,Treatments,Groups,Cmpd_Groupings)

######### Done creating dataframe

#####This exports your mean/stdev to 1 excel spreadsheet, tab 1 is means and tab 2 is stdev
writer = pd.ExcelWriter('Means_And_StDev.xlsx')
df_means.to_excel(writer,'Sheet1')
df_stdev.to_excel(writer,'Sheet2')
writer.save()

#####here we define the panels/tabs
tab1 = bar_tab(df_means,df_stdev, Time,Treatments,number_cmpds_run)
tab2 = single_pie_tab(df_means,df_stdev, Time,Treatments,number_cmpds_run)
tab3 = rings_tab(df_means,df_stdev, Time, Treatments ,number_cmpds_run)
tab4 = radar_tab(df_means,df_stdev, Time,Treatments,number_cmpds_run,Groups)
tab5 = radar_norm_tab(df_means,df_stdev, Time,Treatments,number_cmpds_run,Groups)
tab6 = heatmap_tab(df_means,df_stdev, Time, Treatments ,number_cmpds_run)
tab7 = intervals_tab(df_means,df_stdev, Time, Treatments ,number_cmpds_run)

tabs = Tabs(tabs=[tab1, tab2,tab3,tab4,tab5,tab6, tab7])
curdoc().add_root(tabs)