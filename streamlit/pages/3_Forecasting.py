import io
import json
import pandas as pd
import numpy as np
import folium as fs
import altair as alt

import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder

import streamlit as st
import plotly.express as px
import plotly.graph_objs as go

st.set_page_config(page_title="Forecasting")

st.markdown("<h4 style='color: #0066cc'>Estimate Future Price of Your Ideal Home</h4>", unsafe_allow_html=True)

st.markdown(
    """
    <div style='background-color: #0066cc; padding: 10px'>
        <h2 style='color: white;text-align: center;'>Forecasting Flat Prices</h2>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='background-color: white; padding: 10px'>
    </div>
    """,
    unsafe_allow_html=True
)


# interact with FastAPI endpoint
backend = "http://fastapi:8000/async_predict_prophet"


st.markdown('''
This is a dashboard showing the *forecasted prices* of different types of HDB :house: s
''')


# TODO: Replace with actual options
TOWNS = ["ANG MO KIO", "BEDOK", "BISHAN", "BUKIT BATOK", "BUKIT MERAH", "BUKIT PANJANG", "BUKIT TIMAH", "CENTRAL AREA","CHOA CHU KANG", "CLEMENTI", "GEYLANG", "HOUGANG", "JURONG EAST", "JURONG WEST", "KALLANG/WHAMPOA", "MARINE PARADE", "PASIR RIS", "PUNGGOL", "QUEENSTOWN", "SEMBAWANG", "SENGKANG", "SERANGOON", "TAMPINES", "TOA PAYOH", "WOODLANDS", "YISHUN"]
FLAT_TYPES = ['1 ROOM', '2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', 'MULTI-GENERATION']
EXCLUSIONS = {
    "ANG MO KIO, 1 ROOM", "BEDOK, 1 ROOM", "BISHAN, 1 ROOM", "BUKIT BATOK, 1 ROOM", "BUKIT PANJANG, 1 ROOM", "BUKIT TIMAH, 1 ROOM", "CENTRAL AREA, 1 ROOM", "CHOA CHU KANG, 1 ROOM", "CLEMENTI, 1 ROOM", "GEYLANG, 1 ROOM", "HOUGANG, 1 ROOM", "JURONG EAST, 1 ROOM", "JURONG WEST, 1 ROOM", "KALLANG/WHAMPOA, 1 ROOM", "MARINE PARADE, 1 ROOM", "PASIR RIS, 1 ROOM", "PUNGGOL, 1 ROOM", "QUEENSTOWN, 1 ROOM", "SEMBAWANG, 1 ROOM", "SENGKANG, 1 ROOM", "SERANGOON, 1 ROOM", "TAMPINES, 1 ROOM", "TOA PAYOH, 1 ROOM", "WOODLANDS, 1 ROOM", "YISHUN, 1 ROOM",
    "BISHAN, 2 ROOM", "BUKIT BATOK, 2 ROOM", "BUKIT TIMAH, 2 ROOM", "MARINE PARADE, 2 ROOM",
    "BUKIT MERAH, EXECUTIVE", "CENTRAL AREA, EXECUTIVE", "MARINE PARADE, EXECUTIVE",
    "ANG MO KIO, MULTI-GENERATION", "BEDOK, MULTI-GENERATION", "BUKIT BATOK, MULTI-GENERATION", "BUKIT MERAH, MULTI-GENERATION", "BUKIT PANJANG, MULTI-GENERATION", "BUKIT TIMAH, MULTI-GENERATION", "CENTRAL AREA, MULTI-GENERATION","CHOA CHU KANG, MULTI-GENERATION", "CLEMENTI, MULTI-GENERATION", "GEYLANG, MULTI-GENERATION", "HOUGANG, MULTI-GENERATION", "JURONG EAST, MULTI-GENERATION", "JURONG WEST, MULTI-GENERATION", "KALLANG/WHAMPOA, MULTI-GENERATION", "MARINE PARADE, MULTI-GENERATION", "PASIR RIS, MULTI-GENERATION", "PUNGGOL, MULTI-GENERATION", "QUEENSTOWN, MULTI-GENERATION", "SEMBAWANG, MULTI-GENERATION", "SENGKANG, MULTI-GENERATION", "SERANGOON, MULTI-GENERATION", "TOA PAYOH, MULTI-GENERATION", "WOODLANDS, MULTI-GENERATION"
    }

town_flat_types = [t+', '+ft for ft in FLAT_TYPES for t in TOWNS if t+', '+ft not in EXCLUSIONS]
#town_flat_types = [t+', '+ft for ft in FLAT_TYPES for t in TOWNS]
defaults = town_flat_types[:2]

options = st.multiselect(
    'Select Town and Flat Type',
    town_flat_types,
    defaults,
    max_selections=4)


def concatenated_to_town_flat_type(concatenated):
    splitted = list(map(lambda x: x.split(", "), concatenated))
    towns = [x[0] for x in splitted]
    flat_types = [x[1] for x in splitted]
    return {"town_filter": towns, "flat_type_filter": flat_types}


def dict_to_df(response):
    (town, flat_type, data) = response.items()
    df = pd.DataFrame.from_dict(data[1], orient='index')
    df.index.name = 'date'
    df = df.reset_index()
    df['date'] = pd.to_datetime(df["date"])
    # TODO: Reformat date below
    #df['date'] = pd.to_datetime(df["date"], format='%y%m%d')
    return {"town_flat_type": town[1]+', '+flat_type[1], "data": df}


# Define up to 4 rgb colors
rgb_colors = ['rgb(31, 119, 180)', 'rgb(180, 31, 91)', 'rgb(31, 180, 36)', 'rgb(196, 191, 26)']
rgba_colors = ['rgba(31, 119, 180, 0.3)', 'rgba(180, 31, 91, 0.3)', 'rgba(31, 180, 36, 0.3)', 'rgba(196, 191, 26, 0.3)']
hex_colors = ['#0000FF', '#FF0000', '#00FF00', '#FFFF00']

def make_plots(df_dict, i):
    df = df_dict['data']
    name = df_dict['town_flat_type']
    plot = [
        go.Scatter(
            name=name,
            x=df['date'],
            y=df['yhat'],
            mode='lines',
            #line=dict(color='rgb(31, 119, 180)'),
            line=dict(color=rgb_colors[i])
        ),
        go.Scatter(
            name='Upper Bound',
            x=df['date'],
            y=df['yhat_upper'],
            mode='lines',
            ##marker=dict(color="#444"),
            #marker=dict(color="#0000FF"),
            marker=dict(color=hex_colors[i]),
            line=dict(width=0),
            hoverinfo='skip',
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=df['date'],
            y=df['yhat_lower'],
            mode='lines',
            #marker=dict(color="#444"),
            #marker=dict(color="#0000FF"),
            marker=dict(color=hex_colors[i]),
            line=dict(width=0),
            fillcolor=rgba_colors[i],
            #fillcolor='rgba(31, 119, 180, 0.3)',
            ##fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            hoverinfo='skip',
            showlegend=False
        )
    ]
    return plot


def make_figures(df_dicts):
    plots = [make_plots(df_dict, i) for i, df_dict in enumerate(df_dicts)]
    flattened = [item for sublist in plots for item in sublist]
    fig = go.Figure(flattened)
    fig.update_layout(
         yaxis_title='Price (SGD)',
         title='Forecasted Prices for Town and Flat Type Combinations',
         hovermode="x"
         #xaxis=dict(tickformat="%Y")
     )
    ## TODO: Reactivate once date format is ok
    #fig.update_xaxes(
    #tickformat="%b\n%Y")
    return fig


submitted = st.button('Submit')
if submitted:
    with st.spinner(text="Forecasting Prices..."):
        # Response from FastAPI call; Backend is server url
        # NOTE: Selected Filter is a list
        #data = {"town_filter": selected_town_filter, "flat_type_filter": selected_flat_type_filter}
        data = concatenated_to_town_flat_type(options)
        print(data)
        model_response = requests.post(backend, data=json.dumps(data))
        print("Model Response")
        print(model_response)
        parsed = json.loads(model_response.text)
        #parsed = json.loads(json.loads(model_response.text))
        print("Parsed Items")
        #print(parsed)
        #parsed = [p.items() for p in parsed]
        print(parsed)
        dfs = [dict_to_df(p) for p in parsed]
        #figs = [make_figures(df) for df in dfs]
        fig = make_figures(dfs)
        #data_w_metadata = dfs[0]
        #fig = make_figures(data_w_metadata)
        st.plotly_chart(fig, use_container_width=True)
        #for f in figs:
        #    st.plotly_chart(f, use_container_width=True)