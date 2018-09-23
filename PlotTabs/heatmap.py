# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 19:04:25 2018

@author: Alex
"""

#import packages
import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, Whisker, LabelSet, LinearColorMapper
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.layouts import row,column, widgetbox
from bokeh.models.widgets import Select, Panel, Tabs, CheckboxGroup
from numpy import pi
from natsort import natsorted, index_natsorted, order_by_index
from Funcs.Functions import Mean_Groupings, cmpd_options_func, circ, getOverlap

def heatmap_tab(df_means,df_stdev, Time, Treatments ,number_cmpds_run):
    
    Cmpd0= df_means.columns[len(Treatments)+len(Time)]
    cmpd_options=cmpd_options_func(df_means,len(Treatments)+len(Time),number_cmpds_run)
    df_means=df_means.reindex(index=order_by_index(df_means.index, index_natsorted(df_means[Time[0]])))
    
    if len(Treatments) == 4:
        df_means[Treatments[0]] = df_means[Treatments[0]].astype('str') 
        df_means[Treatments[1]] = df_means[Treatments[1]].astype('str') 
        df_means[Treatments[2]] = df_means[Treatments[2]].astype('str')
        df_means[Treatments[3]] = df_means[Treatments[3]].astype('str')
    elif len(Treatments) == 3: 
        df_means[Treatments[0]] = df_means[Treatments[0]].astype('str') 
        df_means[Treatments[1]] = df_means[Treatments[1]].astype('str') 
        df_means[Treatments[2]] = df_means[Treatments[2]].astype('str')       
    elif len(Treatments) == 2: 
        df_means[Treatments[0]] = df_means[Treatments[0]].astype('str') 
        df_means[Treatments[1]] = df_means[Treatments[1]].astype('str') 
    elif len(Treatments) == 1: 
        df_means[Treatments[0]] = df_means[Treatments[0]].astype('str') 
    
    df_means['Treatment'] = df_means[Time[0]].str.cat(df_means[Treatments], sep=' - ')
    df_stdev['Treatment'] = df_means[Time[0]].str.cat(df_means[Treatments], sep=' - ')
    treatments=list(df_means['Treatment'])
    
    df_m=df_means[['Treatment', Cmpd0]].copy()
    df_m2=df_m.set_index(df_m[df_m.columns[0]].astype(str))
    df_m2.drop(df_m.columns[0], axis=1, inplace=True)
    df_s=df_stdev[['Treatment', Cmpd0]].copy()
    df_s2=df_s.set_index(df_s[df_s.columns[0]].astype(str))
    df_s2.drop(df_s2.columns[0], axis=1, inplace=True)
    
    df_HM = pd.DataFrame(index=df_means['Treatment'], columns=df_means['Treatment'])
    df_HM.index.name = 'Treatment1'
    df_HM.columns.name = 'Treatment2'
    
    for i_t in treatments:
        for j_t in treatments:
            m1=df_m2.loc[i_t,Cmpd0]
            m2=df_m2.loc[j_t,Cmpd0]
            sd1=df_s2.loc[i_t,Cmpd0]
            sd2=df_s2.loc[j_t,Cmpd0]
            a1=[m1-sd1,m1+sd1]
            b1=[m2-sd2,m2+sd2]
            a2=[m1-2*sd1,m1+2*sd1]
            b2=[m2-2*sd2,m2+2*sd2]
            a3=[m1-3*sd1,m1+3*sd1]
            b3=[m2-3*sd2,m2+3*sd2]
            if getOverlap(a1,b1)>0:
                marker='green'
            elif getOverlap(a2,b2)>0:
                marker='yellow'
            elif getOverlap(a3,b3)>0:
                marker='orange'
            else:
                marker='red'
            df_HM.loc[i_t,j_t]=marker
    hm_colors=df_HM.values.reshape(-1).tolist()
    t2=treatments*len(treatments)
    t1=[]
    for tt in treatments:
        for i in range(len(treatments)):
            t1.append(tt)  
    source = ColumnDataSource({'treat1':t1,'treat2':t2,'colors':hm_colors})
    
    p=figure(title="Categorical Heatmap",x_range=treatments, y_range=treatments, plot_height=1000, plot_width=1000)
    p.rect(x='treat1', y='treat2',color='colors', width=1, height=1,line_color='black', line_width=2, source=source)
    p.xaxis.major_label_orientation = np.pi/2
    
    select = Select(title='Select your compound:', value=Cmpd0, options=cmpd_options)
    
    def update_data(attrname, old, new):
        cmpd=select.value
        df_m=df_means[['Treatment', cmpd]].copy()
        df_m2=df_m.set_index(df_m[df_m.columns[0]].astype(str))
        df_m2.drop(df_m.columns[0], axis=1, inplace=True)
        df_s=df_stdev[['Treatment', cmpd]].copy()
        df_s2=df_s.set_index(df_stdev[df_s.columns[0]].astype(str))
        df_s2.drop(df_s2.columns[0], axis=1, inplace=True)
        df_HM = pd.DataFrame(index=df_means['Treatment'], columns=df_means['Treatment'])
        df_HM.index.name = 'Treatment1'
        df_HM.columns.name = 'Treatment2'
        for i_t in treatments:
            for j_t in treatments:
                m1=df_m2.loc[i_t,cmpd]
                m2=df_m2.loc[j_t,cmpd]
                sd1=df_s2.loc[i_t,cmpd]
                sd2=df_s2.loc[j_t,cmpd]
                a1=[m1-sd1,m1+sd1]
                b1=[m2-sd2,m2+sd2]
                a2=[m1-2*sd1,m1+2*sd1]
                b2=[m2-2*sd2,m2+2*sd2]
                a3=[m1-3*sd1,m1+3*sd1]
                b3=[m2-3*sd2,m2+3*sd2]
                if getOverlap(a1,b1)>0:
                    marker='green'
                elif getOverlap(a2,b2)>0:
                    marker='yellow'
                elif getOverlap(a3,b3)>0:
                    marker='orange'
                else:
                    marker='red'
                df_HM.loc[i_t,j_t]=marker
        hm_colors=df_HM.values.reshape(-1).tolist()
        t2=treatments*len(treatments)
        t1=[]
        for tt in treatments:
            for i in range(len(treatments)):
                t1.append(tt)  
        results1 = {'treat1':t1,'treat2':t2,'colors':hm_colors}
        source.data = results1
    
    for w in [select]:
        w.on_change('value', update_data)  

	# Create a row layout
    inputs = widgetbox(select)
    layout=row(inputs, p, width=1500)
    tab = Panel(child=layout, title = 'Heatmap')

    return tab