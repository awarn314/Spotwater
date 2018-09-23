# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 22:42:56 2018

@author: Alex
"""

import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, Whisker, LabelSet,  FixedTicker, LinearAxis, FuncTickFormatter, LegendItem
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.layouts import row,column, widgetbox
from bokeh.models.widgets import Select, Panel, Tabs, CheckboxGroup
from numpy import pi
from bokeh.models import Legend
from natsort import natsorted, index_natsorted, order_by_index
from Funcs.Functions import Mean_Groupings, cmpd_options_func, circ, getOverlap


def intervals_tab(df_means,df_stdev, Time, Treatments ,number_cmpds_run):
    
    len_t=len(Treatments)
    time_vals=df_means[Time[0]].drop_duplicates().tolist()
    time_vals=natsorted(time_vals)
    df_means=df_means.reindex(index=order_by_index(df_means.index, index_natsorted(df_means[Time[0]])))
    cmpd_options=cmpd_options_func(df_means,len_t+1,number_cmpds_run)
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
    def_cmpds=[]
    for i in range(5):
        def_cmpds.append(df_means.columns[len_t+1+i])   
    df_means['Treatment'] = df_means[Time[0]].str.cat(df_means[Treatments], sep=' - ')
    treats=df_means['Treatment'].tolist()
    
    xs=[]
    ys=[]
    delta=0
    err_xs_t = []
    err_ys_t = []
    results={}
    
    for cc, cmpd in enumerate(def_cmpds):
        xs.append(np.linspace(0+delta,(len(treats)-1)+delta,len(treats)))
        delta=delta+.2
        ys.append(df_means[cmpd])
        yerrs=df_stdev[cmpd].tolist()
        err_xs = []
        err_ys = []
        for x, y, yerr in zip(xs[cc], ys[cc], yerrs):
            err_xs.append((x, x))
            err_ys.append((y - yerr, y + yerr))
        err_xs_t.append(err_xs)  
        err_ys_t.append(err_ys) 
        results.update({'x_'+str(cc) : xs[cc]})
        results.update({'y_'+str(cc) : ys[cc]})
        results.update({'xe_'+str(cc) : err_xs_t[cc]})
        results.update({'ye_'+str(cc) : err_ys_t[cc]})
    source = ColumnDataSource(data=results)
    
    pt_colors=['red','blue','green','black','orange']
    ln_colors=['lightcoral','lightblue','lightgreen','gray','peachpuff']    
    p = figure(title='Simple bar chart', plot_height=1000, plot_width=1000)
    for cc, cmpd in enumerate(def_cmpds):
        l_str='Opt'+str(int(cc+1))
        p.multi_line(xs='xe_'+str(cc), ys='ye_'+str(cc), color=ln_colors[cc],line_width=6, line_alpha=.8,source=source)
        p.circle('x_'+str(cc), 'y_'+str(cc), color=pt_colors[cc], size=10, line_alpha=0,legend=l_str,source=source)
    
    x_dict={}
    for x,tr in zip(xs[1],treats):
        x_dict.update({int(x):tr})

    p.xaxis.ticker = xs[0]
    p.xaxis.major_label_overrides = x_dict
    p.xaxis.major_label_orientation = np.pi/2
    p.xgrid[0].ticker=FixedTicker(ticks=np.arange(-.5,len(treats)-.5,len(time_vals)))


    #widget for pie charts
    select = Select(title="Standard Deviation:", value='1', options=['0','1','2','3','4'])
    
    select_c1 = Select(title='Opt1: Select your 1st compound:', value=def_cmpds[0], options=cmpd_options)
    select_c2 = Select(title='Opt2: Select your 2nd compound:', value=def_cmpds[1], options=cmpd_options)
    select_c3 = Select(title='Opt3: Select your 3rd compound:', value=def_cmpds[2], options=cmpd_options)
    select_c4 = Select(title='Opt4: Select your 4th compound:', value=def_cmpds[3], options=cmpd_options)
    select_c5 = Select(title='Opt5: Select your 5th compound:', value=def_cmpds[4], options=cmpd_options)
    
    def update_title(attrname, old, new):
        p.title.text = select.value+'std deviation for' + select_c1.value + ' and ' + select_c2.value+ ' and ' + select_c3.value+ ' and ' + select_c4.value+ ' and ' + select_c5.value
    
    def update_data(attrname, old, new):
        sd=int(select.value)
        xs=[]
        ys=[]
        delta=0
        err_xs_t = []
        err_ys_t = []
        results1={}
        def_cmpds=[select_c1.value,select_c2.value,select_c3.value,select_c4.value,select_c5.value]
        for cc, cmpd in enumerate(def_cmpds):
            xs.append(np.linspace(0+delta,(len(treats)-1)+delta,len(treats)))
            delta=delta+.2
            ys.append(df_means[cmpd])
            yerrs=df_stdev[cmpd].tolist()
            err_xs = []
            err_ys = []
            for x, y, yerr in zip(xs[cc], ys[cc], yerrs):
                err_xs.append((x, x))
                err_ys.append((y - sd*yerr, y + sd*yerr))
            err_xs_t.append(err_xs)  
            err_ys_t.append(err_ys) 
            results1.update({'x_'+str(cc) : xs[cc]})
            results1.update({'y_'+str(cc) : ys[cc]})
            results1.update({'xe_'+str(cc) : err_xs_t[cc]})
            results1.update({'ye_'+str(cc) : err_ys_t[cc]})
        source.data = results1
        
        
    select_c1.on_change('value', update_title)
    select_c2.on_change('value', update_title)
    select_c3.on_change('value', update_title)
    select_c4.on_change('value', update_title)
    select_c5.on_change('value', update_title)
    select.on_change('value', update_title)
    for w in [select_c1,select_c2,select_c3,select_c4,select_c5,select]:
        w.on_change('value', update_data)
   
    ## Set up the widgets for panel 2
    inputs1 = widgetbox(select)
    inputs2 = widgetbox(select_c1,select_c2,select_c3,select_c4,select_c5)    
    
    layout=row(column(inputs1),column(inputs2), p, width=1500)
    tab = Panel(child=layout,title='Intervals')
    
    return tab