# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 19:33:23 2018

@author: Alex
"""

import pandas as pd
import numpy as np

##create a circle from radians and radius
def circ(rad,thetas=np.linspace(0,2*np.pi)):
    yt = (rad) * np.sin(thetas)
    xt = (rad) * np.cos(thetas)
    return xt, yt

def getOverlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))

def cmpd_options_func(df,time_treat,number_cmpds_run):
    cmpd_options=[]
    for col in range(time_treat,number_cmpds_run+time_treat):
        colname = df.columns[col]
        cmpd_options.append(colname)
    return cmpd_options


def clean_df(excel_in,replicate,Treatments):
    #First we read in excel spreadsheet
    xls = pd.ExcelFile(excel_in) #read in data from excel
    df = xls.parse(index_col=None, na_values=['NA']) #convert excel data into dataframe
    df = df.replace(0, float('NaN')) #replace all values of 0 with NaN so they get ignored    
    if len(replicate)==0:    
        first_col_name=df.columns[0]
        df[['Sample', 'Replicate']] = df[first_col_name].str.split('rep', n=1, expand=True)
        df=df.drop(columns=[first_col_name])
        df = df.reindex(columns=['Replicate'] + list(df.columns[:-1]))
        df = df.reindex(columns=['Sample'] + list(df.columns[:-1]))
        df.Replicate.fillna(value=1, inplace=True)
        for treat in Treatments:
            df[treat].fillna(value=0, inplace=True)
    else:
        first_col_name=df.columns[0]
        df=df.rename(index=str, columns={first_col_name: 'Sample', df[replicate].columns[0]: "Replicate"})
    return df

def Put_Cmpds_Into_Grps(master_sheet,Groups):
    Cmpd_Groupings = pd.DataFrame(columns=Groups)
    Master_Cmpd=pd.read_excel(master_sheet, header=None)
    cc_lists=[]
    ll_lens=[]

    for gr in Groups:
        finder=Master_Cmpd.where(Master_Cmpd == gr)
        gr_loc=finder.stack().reset_index().astype(str).drop(0,1).apply(tuple, axis=1).tolist()
        gr_loc_c=int(gr_loc[0][1])
        gr_loc_r=int(gr_loc[0][0])
        beg=gr_loc_r+1
        cell=Master_Cmpd.iloc[beg,gr_loc_c]
        cmpds=[]
        while pd.notnull(cell) and beg<(len(Master_Cmpd)-1):
            cell=Master_Cmpd.iloc[beg,gr_loc_c]
            if pd.notnull(cell):
                cmpds.append(cell)
            beg=beg+1
        cc_lists.append(cmpds)
        ll_lens.append(len(cmpds))

    max_l=max(ll_lens)
    for gr in range(len(Groups)):
        i=ll_lens[gr]
        while i<max_l:
            cc_lists[gr].append('NaN')
            i=i+1
        Cmpd_Groupings[Groups[gr]]=cc_lists[gr]
    return Cmpd_Groupings

def Mean_Groupings(df,number_cmpds_run,Time,Treatments,Groups,Cmpd_Groupings):
    Temp_Treats=[]
    Temp_Treats.extend(Time)
    Temp_Treats.extend(Treatments)
    df_size=df.shape[1]
    index_Cmpd0=df_size-number_cmpds_run  
    df_means=df
    df_stdev=df
    df_means=df_means.groupby(Temp_Treats)[df_means.columns[index_Cmpd0:df_size]].mean().reset_index()
    df_stdev=df.groupby(Temp_Treats)[df.columns[index_Cmpd0:df_size]].std().reset_index()

    for dd in Groups:
        cmpds_in_this_group=[]
        for comp in Cmpd_Groupings[dd]:
            try:
                df[comp]
                cmpds_in_this_group.append(comp)
            except KeyError:
                continue
        df_means[dd]=df_means[cmpds_in_this_group].mean(1)
        df_stdev[dd]=df_stdev[cmpds_in_this_group].std(1)

    return df_means, df_stdev
    