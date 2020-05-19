import pandas as pd
import os
import numpy as np
import datetime as dt
import glob
import calendar 
import pdb
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px


st.title('APP Oriente')

# READ THE DATA FROM FILE === NOT STORED IN SERVER ... YET

# Drop columns
cols_to_drop=['Bar Trend', 'Next Record',
    'Inside Temperature', 'Inside Humidity',
    '10 Min Avg Wind Speed', 'Extra Temperatures', 'Soil Temperatures', 'Leaf Temperatures',
    'Extra Humidties', 'Storm Rain', 'Start Date of current Storm',
    'Month Rain', 'Year Rain', 'Day ET', 'Month ET', 'Year ET',
    'Soil Moistures', 'Leaf Wetnesses', 'Inside Alarms', 'Rain Alarms',
    'Outside Alarms', 'Extra Temp/Hum Alarms', 'Soil & Leaf Alarms',
    'Transmitter Battery Status', 'Console Battery Voltage',
    'Forecast Icons', 'Forecast Rule number', 'Time of Sunrise',
    'Time of Sunset', '<LF> = 0x0A', '<CR> = 0x0D', 'CRC']

#@st.cache
#def load_data():
pth = '/home/esteban/Dropbox/DatosMeteoOriente/'
files_only = glob.glob(pth+'*/*.csv')
#files_only = glob.glob('/home/esteban/Dropbox/Public/streamlit_dataTest/*.csv')
#files_only = glob.glob('/home/esteban/Dropbox/Public/streamlit_dataTest2/*.csv')

data = pd.DataFrame()
for i in files_only: 
    df = pd.read_csv(i) 
    df.drop(cols_to_drop, axis=1, inplace = True)
    data = data.append(df)

# Sort data by date
data.sort_values(by='Tiempo Sistema', inplace=True, ascending=True)

index = np.arange(0,len(data))
data = data.set_index(index) 

# Apply basic transformations
data['Tiempo Sistema'] = pd.to_datetime(data['Tiempo Sistema']) - pd.to_timedelta(5,unit='h')
data['Rain Rate'] = data['Rain Rate']*0.2/10. #in units of cm/hour
data['Barometer'] = data['Barometer']/1000. + 760 # FALTA CORREGIR ESTE CLALCULO
data['Outside Temperature'] = ( data['Outside Temperature']/10. - 32.) * (5.0/9.0)
data.loc[(data['Outside Temperature'] > 50) | (data['Outside Temperature'] < -15)] = np.nan
    
#    return data

# Load de data
#df = load_data()
df = data
#df = pd.read_csv('/home/esteban/Dropbox/DatosMeteoOriente/one_file1.csv')

st.title('Última actualización')

'## Fecha[Y-M-D]/hora',df['Tiempo Sistema'].iloc[-1]
'## Temperatura',round(df['Outside Temperature'].iloc[-1],2),'°C'
'## Presión',df['Barometer'].iloc[-1],'hPa'


st.title('Gráficos')

## Select dates to display plots
min_date_data = pd.to_datetime(df['Tiempo Sistema']).min()
max_date_data = pd.to_datetime(df['Tiempo Sistema']).max()

st.sidebar.markdown('# Fechas plots')
tmp1 = st.sidebar.date_input('Fecha inicial',min_date_data)
tmp2 = st.sidebar.date_input('Fecha final',max_date_data)
ok = ( (pd.to_datetime(df['Tiempo Sistema']) >= pd.to_datetime(tmp1)) & \
       (pd.to_datetime(df['Tiempo Sistema']) <  pd.to_datetime(tmp2)) )

## DF for selected dates
df2 = df[ok]

## Temporal variation of variables
st.sidebar.markdown('# Variable comportamiento temporal')
vars_ops = [ii for ii in df.keys() if ii != 'Tiempo Sistema']
var1 = st.sidebar.selectbox('Variación temporal de',vars_ops)

st.write('Gráfico de ',var1,' entre',tmp1,' y ',tmp2)
time_temp_plt = go.Scattergl(x=df2['Tiempo Sistema'], y=df2[var1], mode = 'markers')
df_plt = [time_temp_plt]
layout = go.Layout(xaxis_title="Date", yaxis_title=var1)
fig = go.Figure(data=df_plt, layout=layout)
st.write(fig)

## Comparison among variables
st.sidebar.markdown('# Variable1 vs Variable2')
vars_ops1 = [ii for ii in df.keys() if ii != 'Tiempo Sistema']
var1 = st.sidebar.selectbox('Var1',vars_ops1,index=4)

vars_ops2 = [ii for ii in df.keys() if ii != 'Tiempo Sistema']
var2 = st.sidebar.selectbox('Var2',vars_ops2,index=5)


ok = ( (pd.to_datetime(df['Tiempo Sistema']) >= pd.to_datetime(tmp1)) & \
       (pd.to_datetime(df['Tiempo Sistema']) <  pd.to_datetime(tmp2)) )

st.write('Gráfico de ',var1,' vs ',var2,' entre',tmp1,' y ',tmp2)
df2 = df[ok]
time_temp_plt = go.Scattergl(x=df2[var1], y=df2[var2], mode = 'markers')
df_plt = [time_temp_plt]
layout = go.Layout(xaxis_title=var1, yaxis_title=var2)
fig = go.Figure(data=df_plt, layout=layout)
st.write(fig)

if st.checkbox('Mostrar datos'):
    '## Data',len(df2)
    df2

#st.write('TEST')
#test = st.multiselect('Varibles',vars_ops)
#st.write(test)


#df3 = df.groupby(by='Tiempo Sistema')

#months = [mm for mm in df['Tiempo Sistema'].dt.month]
#months

###################
###################
# PENDIENTES
# Obtener los meses, días y horas en una variable
# Hacer un gráfico de promedio, stddev, min, max de una variable para un mes
# Colocar todo en recuadros

#st.header("Plotly Presión")
#st.write('Gráfico de presión entre',tmp1,' y ',tmp2)
#time_temp_plt = go.Scatter(x=df2['Tiempo Sistema'], y=df2['Barometer'], mode = 'markers')
#df_plt = [time_temp_plt]
#layout = go.Layout(xaxis_title="Date", yaxis_title="Presión [hpa]")
#fig = go.Figure(data=df_plt, layout=layout)
#st.write(fig)



