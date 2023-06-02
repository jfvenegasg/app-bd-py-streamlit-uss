from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import os
from google.cloud import bigquery

#pip install protobuf==3.20.*

# Aca se define el token para acceder al servicio Bigquery en GCP
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'shiny-apps-385622-08e5b9820326.json'

#Aca se define un cliente para realizar luego la consulta SQL
client = bigquery.Client()

#Esta es la consulta SQL que se realiza(es la misma que hacemos en R)
query = """   SELECT * from `bigquery-public-data.austin_bikeshare.bikeshare_trips` LIMIT 10 """

#Aqui se hace la consulta a BigQuery
query_job = client.query(query)
#Aqui se transforma la consulta en un dataframe
df = query_job.to_dataframe()

"""
# Esta una app de demostración realizada con la libreria StreamLit. Esta app se puede desplegar en contenedores de forma local asi como en la nube.
"""
c=st.empty()
        
        
c.image("uss.png")

st.dataframe(df)

with st.echo(code_location='below'):
    total_points = st.slider("Numero de puntos en el espiral", 1, 5000, 2000)
    num_turns = st.slider("Numero de giros en el espiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))

