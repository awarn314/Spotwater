# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 21:00:45 2018

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


def bar_tab(df_means,df_stdev, Time, Treatments ,number_cmpds_run):
    colors=["firebrick", "navy", 'green', 'orange', 'violet','lawngreen','powderblue','lightgreen', 'yellow','olive','red', 'grey','skyblue','indigo','slategray','hotpink','peachpuff','powderblue']
    Cmpd0= df_means.columns[len(Treatments)+len(Time)]
    cmpd_options=cmpd_options_func(df_means,len(Treatments)+len(Time),number_cmpds_run)
    time_vals=df_means[Time[0]].drop_duplicates().tolist()
    time_vals=natsorted(time_vals)
    df_means=df_means.reindex(index=order_by_index(df_means.index, index_natsorted(df_means[Time[0]])))
    
    MEANs=df_means.groupby(Treatments)[Cmpd0].apply(list).to_dict()
    STDs=df_stdev.groupby(Treatments)[Cmpd0].apply(list).to_dict()
    keys=[]
    u_keys=[]
    l_keys=[]
    results = {'time_vals' : time_vals}

    
    for h in range(len(MEANs)):
        kk=list(MEANs.keys())[h][0]
        for tot in range(1,len(Treatments)):
            sk=list(MEANs.keys())[h][tot]
            if type(sk).__name__ != 'str':
               sk=str(sk) 
            kk += '_' + sk
        keys.append(kk)
        u_keys.append('upper '+kk)
        l_keys.append('lower '+kk)
        mu=list(MEANs.values())[h]
        sd=list(STDs.values())[h]
        upper=[x+e for x,e in zip(mu, sd) ]
        lower=[x-e for x,e in zip(mu, sd) ]
        results.update({keys[h]   : mu})
        results.update({u_keys[h]   : upper})
        results.update({l_keys[h]   : lower})
    source = ColumnDataSource(data=results)
    
    p = figure(x_range=time_vals, plot_height=1000, plot_width=1000, 
               title=Cmpd0, toolbar_location="right")
    legend_it = []
    for hh in range(len(MEANs)):
        c=p.vbar(x=dodge('time_vals', -0.4+(.8*hh/len(MEANs)), range=p.x_range), top=keys[hh], width=(0.8/len(MEANs)), source=source,color=colors[hh])
        p.add_layout(Whisker(source=source, base=dodge('time_vals', -0.4+(.8*hh/len(MEANs)), range=p.x_range), upper=u_keys[hh], lower=l_keys[hh], level="overlay"))
        legend_it.append((keys[hh], [c]))
    legend = Legend(items=legend_it, location=(0, 0))
    legend.click_policy="mute"
    p.add_layout(legend, 'right')
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.orientation = "vertical"
    
    
    #This is where the widget is setup
    select = Select(title='Select your compound:', value=Cmpd0, options=cmpd_options)
    select_sd = Select(title="Standard Deviation:", value='1', options=['0','1','2','3'])
    
    
    def update_title(attrname, old, new):
        p.title.text = select.value
    
    select.on_change('value', update_title)
    
    def update_data(attrname, old, new):
        cmpd=select.value
        std=int(select_sd.value)
        MEANs=df_means.groupby(Treatments)[cmpd].apply(list).to_dict()
        STDs=df_stdev.groupby(Treatments)[cmpd].apply(list).to_dict()
        
        results1 = {'time_vals' : time_vals}
        for y in range(len(MEANs)):
            mu=list(MEANs.values())[y]
            sd=list(STDs.values())[y]
            upper=[x+std*e for x,e in zip(mu, sd) ]
            lower=[x-std*e for x,e in zip(mu, sd) ]
            results1.update({keys[y]   : mu})
            results1.update({u_keys[y]   : upper})
            results1.update({l_keys[y]   : lower})
        source.data = results1
    
    for w in [select,select_sd]:
        w.on_change('value', update_data)  
    
    # Set up layouts and add to document
    inputs = widgetbox(select,select_sd)
    layout=row(column(inputs), p, width=1000)
    tab = Panel(child=layout,title='Bar Charts')

    return tab

