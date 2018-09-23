# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 09:47:19 2018

@author: Alex
"""

#import packages
import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, Whisker, LabelSet
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.layouts import row,column, widgetbox
from bokeh.models.widgets import Select, Panel, Tabs, CheckboxGroup
from numpy import pi
from bokeh.models import Legend, PointDrawTool
from natsort import natsorted, index_natsorted, order_by_index
from Funcs.Functions import Mean_Groupings, cmpd_options_func, circ, getOverlap

def radar_tab(df_means,df_stdev, Time,Treatments,number_cmpds_run,Groups):
    
    colors=["firebrick", "navy", 'green', 'orange', 'violet','skyblue','indigo','slategray','hotpink','peachpuff','powderblue']
    df_means=df_means.reindex(index=order_by_index(df_means.index, index_natsorted(df_means[Time[0]])))
    time_vals=df_means[Time[0]].drop_duplicates().tolist()
    time_vals=natsorted(time_vals)
    def_grps=Groups
    
    if len(Treatments) == 4:
        df_means[Treatments[0]] = df_means[Treatments[0]].astype('str') 
        df_means[Treatments[1]] = df_means[Treatments[1]].astype('str') 
        df_means[Treatments[2]] = df_means[Treatments[2]].astype('str')
        df_means[Treatments[3]] = df_means[Treatments[3]].astype('str')
        tm0_vals=df_means[Treatments[0]].drop_duplicates().tolist()
        tm1_vals=df_means[Treatments[1]].drop_duplicates().tolist()
        tm2_vals=df_means[Treatments[2]].drop_duplicates().tolist()
        tm3_vals=df_means[Treatments[3]].drop_duplicates().tolist()
    elif len(Treatments) == 3: 
        df_means[Treatments[0]] = df_means[Treatments[0]].astype('str') 
        df_means[Treatments[1]] = df_means[Treatments[1]].astype('str') 
        df_means[Treatments[2]] = df_means[Treatments[2]].astype('str')
        tm0_vals=df_means[Treatments[0]].drop_duplicates().tolist()
        tm1_vals=df_means[Treatments[1]].drop_duplicates().tolist()
        tm2_vals=df_means[Treatments[2]].drop_duplicates().tolist()
    elif len(Treatments) == 2: 
        df_means[Treatments[0]] = df_means[Treatments[0]].astype('str') 
        df_means[Treatments[1]] = df_means[Treatments[1]].astype('str') 
        tm0_vals=df_means[Treatments[0]].drop_duplicates().tolist()
        tm1_vals=df_means[Treatments[1]].drop_duplicates().tolist()
    elif len(Treatments) == 1: 
        df_means[Treatments[0]] = df_means[Treatments[0]].astype('str') 
        tm0_vals=df_means[Treatments[0]].drop_duplicates().tolist() 
    
    #norm_fac=100/np.max(df_means[Groups].max())
    #def_grps2=[]
    #for gr in Groups:
    #    new_str='norm_'+gr
    #    df_means[new_str]=norm_fac*df_means[gr]
    #for gr in def_grps:
    #    new_str='norm_'+gr
    #    def_grps2.append(new_str)
    num_vars = len(def_grps)
    
    theta_label = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    theta_label += np.pi/2 # rotate theta such that the first axis is at the top
    
    flist=[]
    
    for tt, tt_str in enumerate(time_vals):
        if len(Treatments) == 4:
            df_for_radar=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==tm0_vals[0]) & (df_means[Treatments[1]]==tm1_vals[0]) & (df_means[Treatments[2]]==tm2_vals[0]) & (df_means[Treatments[3]]==tm3_vals[0])]
        elif len(Treatments) == 3: 
            df_for_radar=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==tm0_vals[0]) & (df_means[Treatments[1]]==tm1_vals[0]) & (df_means[Treatments[2]]==tm2_vals[0]) ]        
        elif len(Treatments) == 2: 
            df_for_radar=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==tm0_vals[0]) & (df_means[Treatments[1]]==tm1_vals[0]) ]
        elif len(Treatments) == 1: 
            df_for_radar=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==tm0_vals[0]) ]
        df_radar_values=df_for_radar[def_grps]
        radar_vals=list(df_radar_values.values.flatten())
        flist.append(radar_vals)
    rad_of_circ=max(df_means[Groups].max())
    x_label,y_label =  circ(rad_of_circ,theta_label)
    x_vals,y_vals=circ(rad_of_circ)
    
    radars={}
    x_t_str=[]
    y_t_str=[]
    for i in range(len(time_vals)):
        x_t_str.append('x_'+time_vals[i])
        y_t_str.append('y_'+time_vals[i])
        xt,yt=circ(flist[i],theta_label)
        radars.update({x_t_str[i]: xt})
        radars.update({y_t_str[i]: yt})
    radars.update({'thetas': theta_label})
    radars.update({'x_label':x_label})
    radars.update({'y_label':y_label})
    radars.update({'text': def_grps})
         
    p = figure(title="Radar",match_aspect=True, plot_height=1000, plot_width=1000)
    source4=ColumnDataSource(data=radars)
    labels = LabelSet(x="x_label",y="y_label",text="text",source=source4)
    p.add_layout(labels)
    p.line(x_vals, y_vals, line_width=3,color='black')
    for i in range(len(time_vals)):
        p.patch(x=x_t_str[i], y=y_t_str[i], fill_alpha=0, line_color=colors[i], line_width=3,source=source4)
    
    #widget for radar charts   
    if len(Treatments) == 4:
        select0 = Select(title=Treatments[0], value=str(tm0_vals[0]), options=tm0_vals)
        select1 = Select(title=Treatments[1], value=str(tm1_vals[0]), options=tm1_vals)
        select2 = Select(title=Treatments[2], value=str(tm2_vals[0]), options=tm2_vals)
        select3 = Select(title=Treatments[3], value=str(tm3_vals[0]), options=tm3_vals)
    elif len(Treatments) == 3: 
        select0 = Select(title=Treatments[0], value=str(tm0_vals[0]), options=tm0_vals)
        select1 = Select(title=Treatments[1], value=str(tm1_vals[0]), options=tm1_vals)
        select2 = Select(title=Treatments[2], value=str(tm2_vals[0]), options=tm2_vals)
    elif len(Treatments) == 2: 
        select0 = Select(title=Treatments[0], value=str(tm0_vals[0]), options=tm0_vals)
        select1 = Select(title=Treatments[1], value=str(tm1_vals[0]), options=tm1_vals) 
    elif len(Treatments) == 1: 
        select0 = Select(title=Treatments[0], value=str(tm0_vals[0]), options=tm0_vals)
    checkbox_group = CheckboxGroup(
            labels=Groups, active=[0, 1, 2, 3, 4, 5])
    
    if len(Treatments) == 4:
        def update_title(attrname, old, new):
            p.title.text = select0.value+' '+select1.value+' '+select2.value+' '+select3.value
    elif len(Treatments) == 3: 
        def update_title(attrname, old, new):
            p.title.text = select0.value+' '+select1.value+' '+select2.value
    elif len(Treatments) == 2: 
        def update_title(attrname, old, new):
            p.title.text = select0.value+' '+select1.value
    elif len(Treatments) == 1: 
        def update_title(attrname, old, new):
            p.title.text = select0.value
    
    def update_data(attrname, old, new):
        compounds_in_radar=[]
        for i in checkbox_group.active:
            compounds_in_radar.append(Groups[i])
        theta_label = np.linspace(0, 2*np.pi, len(compounds_in_radar), endpoint=False)
        theta_label += np.pi/2 # rotate theta such that the first axis is at the top
        flist=[]
        for tt, tt_str in enumerate(time_vals): 
            if len(Treatments) == 4:
                df_for_radar=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==select0.value) & (df_means[Treatments[1]]==select1.value) & (df_means[Treatments[2]]==select2.value) & (df_means[Treatments[3]]==select3.value)]
            elif len(Treatments) == 3: 
                df_for_radar=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==select0.value) & (df_means[Treatments[1]]==select1.value) & (df_means[Treatments[2]]==select2.value) ]        
            elif len(Treatments) == 2: 
                df_for_radar=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==select0.value) & (df_means[Treatments[1]]==select1.value) ]
            elif len(Treatments) == 1:
                df_for_radar=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==select0.value) ]
            df_radar_values=df_for_radar[compounds_in_radar]
            radar_vals=list(df_radar_values.values.flatten())
            if not radar_vals:
                radar_vals=[0]*len(compounds_in_radar)
            flist.append(radar_vals)
        x_label, y_label = circ(rad_of_circ,theta_label)
        radars_res={}
        x_t_str=[]
        y_t_str=[]
        for i in range(len(time_vals)):
                x_t_str.append('x_'+time_vals[i])
                y_t_str.append('y_'+time_vals[i])
                xt,yt=circ(flist[i],theta_label)
                radars_res.update({x_t_str[i]: xt})
                radars_res.update({y_t_str[i]: yt})
        radars_res.update({'thetas' : theta_label})
        radars_res.update({'x_label':x_label})
        radars_res.update({'y_label':y_label})
        radars_res.update({'text': compounds_in_radar})
        source4.data=radars_res
        
    if len(Treatments) == 4:
        select0.on_change('value', update_title)
        select1.on_change('value', update_title)
        select2.on_change('value', update_title)
        select3.on_change('value', update_title)
    elif len(Treatments) == 3: 
        select0.on_change('value', update_title)
        select1.on_change('value', update_title)
        select2.on_change('value', update_title)
    elif len(Treatments) == 2: 
        select0.on_change('value', update_title)
        select1.on_change('value', update_title)
    elif len(Treatments) == 1: 
        select0.on_change('value', update_title)
      
    if len(Treatments) == 4:
        for w in [select0,select1,select2,select3]:
            w.on_change('value', update_data)
    elif len(Treatments) == 3:  
        for w in [select0,select1,select2]:
            w.on_change('value', update_data)
    elif len(Treatments) == 2:  
        for w in [select0,select1]:
            w.on_change('value', update_data)
    elif len(Treatments) == 1:  
        for w in [select0]:
            w.on_change('value', update_data)
        
    checkbox_group.on_change('active', update_data)    
    ## Set up the widgets for panel 2
    if len(Treatments) == 4:
        inputs1 = widgetbox(select0,select1,select2,select3)
    elif len(Treatments) == 3: 
        inputs1 = widgetbox(select0,select1,select2)
    elif len(Treatments) == 2: 
        inputs1 = widgetbox(select0,select1)
    elif len(Treatments) == 1: 
        inputs1 = widgetbox(select0)
    inputs2 = widgetbox(checkbox_group)    
    #### this completes the 4th tab with radar chart
    
    layout=row(column(inputs1),inputs2, p, width=1500)
    tab = Panel(child=layout,title='Radar Chart')
    
    return tab