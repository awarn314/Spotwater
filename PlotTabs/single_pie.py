# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 22:46:04 2018

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
from bokeh.models import Legend
from natsort import natsorted, index_natsorted, order_by_index
from Funcs.Functions import Mean_Groupings, cmpd_options_func, circ, getOverlap

def single_pie_tab(df_means,df_stdev, Time, Treatments ,number_cmpds_run):
    
    len_t=len(Treatments)
    
    colors=["firebrick", "navy", 'green', 'orange', 'violet','lawngreen','lightgreen', 'yellow','olive','red', 'grey','skyblue','indigo','slategray','hotpink','peachpuff','powderblue']
    
    df_means=df_means.reindex(index=order_by_index(df_means.index, index_natsorted(df_means[Time[0]])))
    cmpd_options=cmpd_options_func(df_means,len_t+1,number_cmpds_run)
    
    time_vals=df_means[Time[0]].drop_duplicates().tolist()
    if len(Treatments) == 4:
        df_means[Treatments[0]] = df_means[Treatments[0]].astype('str') 
        df_means[Treatments[1]] = df_means[Treatments[1]].astype('str') 
        df_means[Treatments[2]] = df_means[Treatments[2]].astype('str')
        df_means[Treatments[3]] = df_means[Treatments[3]].astype('str')
        tm0_vals=df_means[Treatments[0]].drop_duplicates().tolist()
        tm1_vals=df_means[Treatments[1]].drop_duplicates().tolist()
        tm2_vals=df_means[Treatments[2]].drop_duplicates().tolist()
        tm3_vals=df_means[Treatments[3]].drop_duplicates().tolist()
        df_for_pie=df_means.loc[(df_means[Time[0]] == time_vals[0]) & (df_means[Treatments[0]]==tm0_vals[0]) & (df_means[Treatments[1]]==tm1_vals[0]) & (df_means[Treatments[2]]==tm2_vals[0]) & (df_means[Treatments[3]]==tm3_vals[0])]
    elif len(Treatments) == 3: 
        df_means[Treatments[0]] = df_means[Treatments[0]].astype('str') 
        df_means[Treatments[1]] = df_means[Treatments[1]].astype('str') 
        df_means[Treatments[2]] = df_means[Treatments[2]].astype('str')
        tm0_vals=df_means[Treatments[0]].drop_duplicates().tolist()
        tm1_vals=df_means[Treatments[1]].drop_duplicates().tolist()
        tm2_vals=df_means[Treatments[2]].drop_duplicates().tolist()
        df_for_pie=df_means.loc[(df_means[Time[0]] == time_vals[0]) & (df_means[Treatments[0]]==tm0_vals[0]) & (df_means[Treatments[1]]==tm1_vals[0]) & (df_means[Treatments[2]]==tm2_vals[0]) ]        
    elif len(Treatments) == 2: 
        df_means[Treatments[0]] = df_means[Treatments[0]].astype('str') 
        df_means[Treatments[1]] = df_means[Treatments[1]].astype('str') 
        tm0_vals=df_means[Treatments[0]].drop_duplicates().tolist()
        tm1_vals=df_means[Treatments[1]].drop_duplicates().tolist()
        df_for_pie=df_means.loc[(df_means[Time[0]] == time_vals[0]) & (df_means[Treatments[0]]==tm0_vals[0]) & (df_means[Treatments[1]]==tm1_vals[0]) ]
    elif len(Treatments) == 1: 
        df_means[Treatments[0]] = df_means[Treatments[0]].astype('str') 
        tm0_vals=df_means[Treatments[0]].drop_duplicates().tolist() 
        df_for_pie=df_means.loc[(df_means[Time[0]] == time_vals[0]) & (df_means[Treatments[0]]==tm0_vals[0]) ]
    df_means = df_means.replace(float('nan'),0)
    def_cmpds=[]
    for i in range(5):
        def_cmpds.append(df_means.columns[len_t+1+i])
    len_cmpds=len(def_cmpds)
    df_pie_values=df_for_pie[def_cmpds]
    pie_vals=list(df_pie_values.values.flatten())
    pie_fracs = [x / sum(pie_vals) for x in pie_vals]
    percents=[0]
    per_labels=[]
    for f in range(0,len(pie_fracs)):
        ff=percents[f]+pie_fracs[f]
        percents.append(ff)
        per_labels.append(df_means.columns[len_t+1+f]+':'+str("{0:0.1f}".format(100.0*pie_fracs[f])))
    ss=[per*2*pi for per in percents[:-1]]
    ee=[per*2*pi for per in percents[1:]]
    mid=[]
    for pp in range(len(ss)):
        mid.append(.5*ss[pp]+.5*ee[pp])
    cc=colors[0:len_cmpds]
    source = ColumnDataSource(data=dict(starts=ss, ends=ee, color=cc))
    x_label, y_label=circ(.5,mid)
    p_label_data = ColumnDataSource({'x_label':x_label,'y_label':y_label,'p_labels':per_labels})
    p = figure(match_aspect=True, plot_height=1000, plot_width=1000)
    x_vals,y_vals=circ(1)
    p.line(x_vals, y_vals, line_width=5,color='black')
    p.wedge(x=0, y=0, radius=1, start_angle='starts', end_angle='ends', color='color',source=source)
    p_labels = LabelSet(x="x_label",y="y_label",text="p_labels",source=p_label_data, text_color='black')
    p.add_layout(p_labels)
    
    
    #widget for pie charts
    sel_t = Select(title="Choose a time:", value=time_vals[0], options=time_vals)
    
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
        
    checkbox_group = CheckboxGroup(labels=cmpd_options, active=[0, 1, 2, 3, 4])
    
    def update_data(attrname, old, new):
        if len(Treatments) == 4:
            df_for_pie=df_means.loc[(df_means[Time[0]] == sel_t.value) & (df_means[Treatments[0]]==select0.value) & (df_means[Treatments[1]]==select1.value) & (df_means[Treatments[2]]==select2.value) & (df_means[Treatments[3]]==select3.value)]
        elif len(Treatments) == 3: 
            df_for_pie=df_means.loc[(df_means[Time[0]] == sel_t.value) & (df_means[Treatments[0]]==select0.value) & (df_means[Treatments[1]]==select1.value) & (df_means[Treatments[2]]==select2.value) ]        
        elif len(Treatments) == 2: 
            df_for_pie=df_means.loc[(df_means[Time[0]] == sel_t.value) & (df_means[Treatments[0]]==select0.value) & (df_means[Treatments[1]]==select1.value) ]
        elif len(Treatments) == 1:
            df_for_pie=df_means.loc[(df_means[Time[0]] == sel_t.value) & (df_means[Treatments[0]]==select0.value) ]
        compounds_in_pie=[]
        for i in checkbox_group.active:
            compounds_in_pie.append(cmpd_options[i])
            
        df_pie_values=df_for_pie[compounds_in_pie]
        pie_vals=list(df_pie_values.values.flatten())
        pie_fracs = [x / sum(pie_vals) for x in pie_vals]
        percents=[0]
        per_labels=[]
        for f in range(0,len(pie_fracs)):
            ff=percents[f]+pie_fracs[f]
            percents.append(ff)
            per_labels.append(compounds_in_pie[f]+':'+str("{0:0.1f}".format(100.0*pie_fracs[f])))
        starts = [per*2*pi for per in percents[:-1]]
        ends = [per*2*pi for per in percents[1:]]
        if len(ends)==0:
            ends=[0] * len(compounds_in_pie)
            starts=[0] * len(compounds_in_pie)
            #per_labels=[0] * len(compounds_in_pie)
            #per_labels=['{:.2f}'.format(x) for x in per_labels]
        mid=[]
        for pp in range(len(starts)):
            mid.append(.5*starts[pp]+.5*ends[pp])
        pie_colors=colors[0:len(compounds_in_pie)]
        x_label, y_label=circ(.5,mid)
        result2_label={'x_label':x_label,
                       'y_label':y_label,
                       'p_labels':per_labels}
        result2={'starts' : starts,
                'ends'   : ends,
                'color'  : pie_colors}
        source.data=result2
        p_label_data.data=result2_label
    
    if len(Treatments) == 4:
        for w in [sel_t,select0,select1,select2,select3]:
            w.on_change('value', update_data)
    elif len(Treatments) == 3:  
        for w in [sel_t,select0,select1,select2]:
            w.on_change('value', update_data)
    elif len(Treatments) == 2:  
        for w in [sel_t,select0,select1]:
            w.on_change('value', update_data)
    elif len(Treatments) == 1:  
        for w in [sel_t,select0]:
            w.on_change('value', update_data)

    checkbox_group.on_change('active', update_data)    
    
    ## Set up the widgets for pie
    if len(Treatments) == 4:
        inputs1 = widgetbox(sel_t,select0,select1,select2,select3)
    elif len(Treatments) == 3: 
        inputs1 = widgetbox(sel_t,select0,select1,select2)
    elif len(Treatments) == 2: 
        inputs1 = widgetbox(sel_t,select0,select1)
    elif len(Treatments) == 1: 
        inputs1 = widgetbox(sel_t,select0)
    inputs2 = widgetbox(checkbox_group)

    # Set up layouts and add to document
    layout=row(column(inputs1),inputs2, p, width=1500)
    tab = Panel(child=layout,title='Pie Charts')

    return tab