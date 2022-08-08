import altair as alt
import pandas as pd
import numpy as np
import streamlit as st

st.title("Evolución de la Tasa de mujeres respecto a la cantidad total de trabajadores de una empresa")

df = pd.read_csv('https://raw.githubusercontent.com/TamaraESS/Viz-MIA-UC/main/Base_Proyecto_3.csv',delimiter=";")

df2 = df.sample(frac=0.5)
df2['YEAR']=df2['YEAR'].astype(int)
df2['Tasa_Mujer']=df2['MUJERES']/df2['ID']

st.write('En estas gráficas se observa inicialmente la cantidad de trabajadores')
st.write('totales de una empresa versus la proporción de mujeres en cada periodo.')
st.write('Los datos son aperturados por los distintos grupos etarios.')

sel = alt.selection(type="interval", encodings=['x'])

trab = alt.Chart(df2).mark_bar().encode(
    x=alt.X('YEAR',bin=alt.Bin(step=0.5), scale=alt.Scale(domain=[2010,2017])),
    y='sum(ID):Q',
    color='Rango Edad:N'
).properties(
    width=180,
    height=180
).facet(
    title='Cantidad Total de Trabajadores por cada grupo etario desde 2010 a 2016',
    column='Rango Edad:N'
).transform_filter(
    sel
)

edad = alt.Chart(df2).mark_bar().encode(
    x='Rango Edad:N',
    y='sum(ID):Q',
    color=alt.condition(sel, alt.ColorValue("darkgrey"), alt.ColorValue("lightgrey"))
).properties(
    width=180,
    height=180
).add_selection(sel)

a=alt.vconcat(
    trab,
    edad
).resolve_legend(
    color="independent",
    size="independent"
)
#st.write('Evolución de la Tasa de mujeres por cada grupo etario desde 2010 hasta 2016')
sel = alt.selection(type="interval", encodings=['x'])

muj = alt.Chart(df2).mark_line().encode(
    x=alt.X('YEAR',bin=alt.Bin(step=0.5), scale=alt.Scale(domain=[2010,2017])),
    y='mean(Tasa_Mujer):Q',
    color='Rango Edad:N'
).properties(
    width=180,
    height=180
).facet(
    title='Evolución de la Tasa de mujeres por cada grupo etario desde 2010 hasta 2016',
    column='Rango Edad:N'
).transform_filter(
    sel
)

edad2 = alt.Chart(df2).mark_bar().encode(
    x='Rango Edad:N',
    y='sum(ID):Q',
    color=alt.condition(sel, alt.ColorValue("pink"), alt.ColorValue("lightgrey"))
).properties(
    width=180,
    height=180
).add_selection(sel)

b=alt.vconcat(
    muj,
    edad2
).resolve_legend(
    color="independent",
    size="independent"
)
c = a & b

st.altair_chart(c, use_container_width=True)