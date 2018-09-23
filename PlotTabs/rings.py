# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 11:59:03 2018

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

def rings_tab(df_means,df_stdev, Time, Treatments ,number_cmpds_run):
    
    len_t=len(Treatments)
    
    colors=["firebrick", "navy", 'green', 'orange', 'violet','lawngreen','lightgreen', 'yellow','olive','red', 'grey','skyblue','indigo','slategray','hotpink','peachpuff','powderblue']
    
    df_means=df_means.reindex(index=order_by_index(df_means.index, index_natsorted(df_means[Time[0]])))
    cmpd_options=cmpd_options_func(df_means,len_t+1,number_cmpds_run)
    
    time_vals=df_means[Time[0]].drop_duplicates().tolist()
    time_vals=natsorted(time_vals)
    
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
    df_means = df_means.replace(float('nan'),0)
    start_keys=[]
    end_keys=[]
    mid_keys=[]
    per_keys=[]
    for h in time_vals:
        start_keys.append('start '+h)
        end_keys.append('end '+h)
        mid_keys.append('mid '+h)
        per_keys.append('per '+h)
    
    def_cmpds=[]
    for i in range(5):
        def_cmpds.append(df_means.columns[len_t+1+i])
    len_cmpds=len(def_cmpds)
    
    p=figure(match_aspect=True, plot_height=1000, plot_width=1000)

    starts=[]
    ends=[]
    mid=[]
    per_labels=[]
    ring_colors=colors[0:len_cmpds]
    results3 = {'color'  : ring_colors}
    labels_dicts={}
    p_x_strs=[]
    p_y_strs=[]
    
    for tt, tt_str in enumerate(time_vals):
        if len(Treatments) == 4:
            df_for_ring=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==tm0_vals[0]) & (df_means[Treatments[1]]==tm1_vals[0]) & (df_means[Treatments[2]]==tm2_vals[0]) & (df_means[Treatments[3]]==tm3_vals[0])]
        elif len(Treatments) == 3: 
            df_for_ring=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==tm0_vals[0]) & (df_means[Treatments[1]]==tm1_vals[0]) & (df_means[Treatments[2]]==tm2_vals[0]) ]        
        elif len(Treatments) == 2: 
            df_for_ring=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==tm0_vals[0]) & (df_means[Treatments[1]]==tm1_vals[0]) ]
        elif len(Treatments) == 1: 
            df_for_ring=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==tm0_vals[0]) ]
        df_ring_values=df_for_ring[def_cmpds]
        ring_vals=list(df_ring_values.values.flatten())
        ring_sums=sum(ring_vals)
        ring_fracs = [x / ring_sums for x in ring_vals]
        percents=[0]
        perper_labels=[]
        for f in range(0,len(ring_fracs)):
            ff=percents[f]+ring_fracs[f]
            percents.append(ff)
            if tt==(len(time_vals)-1):
                perper_labels.append(def_cmpds[f]+': '+str("{0:0.1f}".format(100.0*ring_fracs[f])))
            else:
                perper_labels.append(str("{0:0.1f}".format(100.0*ring_fracs[f])))
        per_labels.append(perper_labels)
        starts=[per*2*pi for per in percents[:-1]]
        ends=[per*2*pi for per in percents[1:]]
        mid=[]
        for pp in range(len(starts)):
            mid.append(.5*starts[pp]+.5*ends[pp])
        results3.update({start_keys[tt]:starts})
        results3.update({end_keys[tt]:ends})
        results3.update({mid_keys[tt]:mid})
        labels_dicts.update({per_keys[tt]:list(per_labels[tt])})
        x_label, y_label=circ(.5+tt,mid)
        x_str='xlabel_'+str(tt)
        p_x_strs.append(x_str)
        y_str='ylabel_'+str(tt)
        p_y_strs.append(y_str)
        labels_dicts.update({x_str:x_label})
        labels_dicts.update({y_str:y_label})
    source3 = ColumnDataSource(data=results3)
    p_label_source=ColumnDataSource(data=labels_dicts)
    for tt, tt_str in enumerate(time_vals):
        p.annular_wedge(x=0, y=0, inner_radius=tt, outer_radius=tt+1, start_angle=start_keys[tt], end_angle=end_keys[tt], color='color',source=source3)
        x_vals,y_vals=circ(tt+1)
        p.line(x_vals, y_vals, line_width=3,color='black')
        p_labels = LabelSet(x=p_x_strs[tt],y=p_y_strs[tt],text=per_keys[tt],source=p_label_source)
        p.add_layout(p_labels)

    #widget for ring charts     
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
            labels=cmpd_options, active=[0, 1, 2, 3, 4])

    #widget for ring charts     
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

    #widget for ring charts     
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

    def update_data(attrname, old, new):
        compounds_in_ring=[]
        for i in checkbox_group.active:
            compounds_in_ring.append(cmpd_options[i])
        ring_colors=colors[0:len(compounds_in_ring)]
        starts=[]
        ends=[]
        mid=[]
        per_labels=[]
        results3 = {'color'  : ring_colors}
        labels_dicts={}
        p_x_strs=[]
        p_y_strs=[]
        for tt, tt_str in enumerate(time_vals): 
            if len(Treatments) == 4:
                df_for_ring=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==select0.value) & (df_means[Treatments[1]]==select1.value) & (df_means[Treatments[2]]==select2.value) & (df_means[Treatments[3]]==select3.value)]
            elif len(Treatments) == 3: 
                df_for_ring=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==select0.value) & (df_means[Treatments[1]]==select1.value) & (df_means[Treatments[2]]==select2.value) ]        
            elif len(Treatments) == 2: 
                df_for_ring=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==select0.value) & (df_means[Treatments[1]]==select1.value) ]
            elif len(Treatments) == 1:
                df_for_ring=df_means.loc[(df_means[Time[0]] == tt_str) & (df_means[Treatments[0]]==select0.value) ]
          
            df_ring_values=df_for_ring[compounds_in_ring]
            ring_vals=list(df_ring_values.values.flatten())
            ring_sums=sum(ring_vals)
            ring_fracs = [x / ring_sums for x in ring_vals]
            percents=[0]
            perper_labels=[]
            for f in range(0,len(ring_fracs)):
                ff=percents[f]+ring_fracs[f]
                percents.append(ff)
                if tt==(len(time_vals)-1):
                    perper_labels.append(compounds_in_ring[f]+': '+str("{0:0.1f}".format(100.0*ring_fracs[f])))
                else:
                    perper_labels.append(str("{0:0.1f}".format(100.0*ring_fracs[f])))
            per_labels.append(perper_labels)
            starts=[per*2*pi for per in percents[:-1]]
            ends=[per*2*pi for per in percents[1:]]
            if len(ends)==0:
                ends=[0] * len(compounds_in_ring)
                starts=[0] * len(compounds_in_ring)
                #per_labels=[0] * len(compounds_in_pie)
                #per_labels=['{:.2f}'.format(x) for x in per_labels]
            mid=[]
            for pp in range(len(starts)):
                mid.append(.5*starts[pp]+.5*ends[pp]) 
            results3.update({start_keys[tt]:starts})
            results3.update({end_keys[tt]:ends})
            results3.update({mid_keys[tt]:mid})
            labels_dicts.update({per_keys[tt]:list(per_labels[tt])})
            x_label, y_label=circ(.5+tt,mid)
            x_str='xlabel_'+str(tt)
            p_x_strs.append(x_str)
            y_str='ylabel_'+str(tt)
            p_y_strs.append(y_str)
            labels_dicts.update({x_str:x_label})
            labels_dicts.update({y_str:y_label})
        p_label_source.data=labels_dicts
        source3.data=results3
         
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
    
    ## Set up the widgets for rings
    if len(Treatments) == 4:
        inputs1 = widgetbox(select0,select1,select2,select3)
    elif len(Treatments) == 3: 
        inputs1 = widgetbox(select0,select1,select2)
    elif len(Treatments) == 2: 
        inputs1 = widgetbox(select0,select1)
    elif len(Treatments) == 1: 
        inputs1 = widgetbox(select0)
    inputs2 = widgetbox(checkbox_group)

    layout=row(column(inputs1),inputs2, p, width=1500)
    tab = Panel(child=layout, title="Pie in Pie Chart")
    return tab