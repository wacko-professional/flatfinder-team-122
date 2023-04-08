import streamlit as st
import plotly.express as px
import pandas as pd
import base64
import time

st.set_page_config(layout="wide", page_title="Welcome")
########################################################################################################################


# https://soundcloud.com/ashamaluevmusic/imagination
# https://github.com/streamlit/streamlit/issues/2446
# def autoplay_audio(file_path: str):
#     with open(file_path, "rb") as f:
#         data = f.read()
#         b64 = base64.b64encode(data).decode()
#         md = f"""
#             <audio controls autoplay="true" loop="true">
#             <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
#             </audio>
#             """
#         st.markdown(
#             md,
#             unsafe_allow_html=True,
#         )

col1, mid, col2 = st.columns([1,1.5,20])
with col1:
    st.image('logo.png', width = 50)
with col2:
    original_title = '<h1 style ="font-weight: bold;position: relative; bottom: 10px;color:#0066cc; font-size: 28px;">FlatFinder</h1>'
    st.markdown(original_title, unsafe_allow_html=True)
# with col3:
#     autoplay_audio("Imagination.mp3")


st.markdown(
    """
    <div style='background-color: #0066cc; padding: 30px'>
        <h2 style='color: white;'>Welcome to FlatFinder!</h2>
        <p style='color: white;'>Plan your next home in 4 simple steps</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='padding: 1px'>
        <h4 style='color: white;color: #808080;text-align: left;'>Observe how the home prices in each town changes over the years</h4>
    </div>
    """,
    unsafe_allow_html=True
)



######################################################################################################

map4 = pd.read_csv("map4.csv")

figure = px.scatter(map4, x='Price/sqm (S$)', y='Distance from city center in km', animation_frame="year",
                    size='scale',
                    color='Price/sqm (S$)', range_x = [1900, 7100],range_y = [-1, 19],
                    title='Minimize sidebar on the left for a better view    •      '
                    'Click on the bubble to select town<br>'
                          'Color represent price per square meter    •      '
                          'Size represent transaction count<br>',
                    log_x=False, size_max=45, text='town', opacity = 0.6,
                    color_continuous_scale='YlGnBu',
                    hover_data={
                                    'town': True,
                                    'year': True,
                                    'Distance from city center in km': False,
                                    'transaction_count': True,
                                    'scale': False},
                        labels={'year': 'Year','town': 'Town ',
                                'transaction_count': 'Number of transactions'}


                    )

figure.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
figure.update_traces(textposition='bottom center', textfont_size=10, textfont_color = '#808080')
figure.update_layout(width=700, height=700, title_font_color='#808080',
                    title_x=0, plot_bgcolor="white",
                    paper_bgcolor="white", clickmode='event+select',
                    xaxis=dict(showgrid=True, gridcolor="lightgrey"),
                    yaxis=dict(showgrid=True, gridcolor="lightgrey")
                     )

def update_color(trace, points, selector):
    c = list(trace.marker.color)
    for i in points.point_inds:
        c[i] = '#FF69B4'  # Set selected point color to pink
    trace.marker.color = c

figure.data[0].on_selection(update_color)

col1, col2, col3 = st.columns([0.5,10,0.5])
with col1:
    st.write(" ")
with col2:
    st.plotly_chart(figure, use_container_width=True)

with col3:
    st.write(" ")

####################################################################################################3

observation = """
The above plot illustrates the housing prices of various towns in Singapore based on their distance from the city center. Darker colors indicate higher prices, and smaller bubbles represent fewer transactions. Homes located closer to the city center have higher prices but fewer transactions, whereas those farther away are cheaper and have more transactions.

Over time, the prices of HDB resale properties in Singapore have increased, with a drop in housing prices beginning in 2013. The pandemic in 2020 caused an increase in demand for housing, resulting in further price appreciation.

Several towns such as Bishan, Ang Mo Kio, Toa Payoh, and Tampines, have experienced steady price increases, while others, such as Punggol and Sengkang, have seen a more significant acceleration in prices recently.

The prices of housing in Singapore have generally increased over time, with fluctuations and variations across different towns.
"""
def typewriter(text):
    t = st.empty()
    for i in range(len(text)):
        t.write(text[:i+1])
        time.sleep(0.05)
        if i == len(text) - 1:
            time.sleep(1) # wait for 1 second after the text is fully displayed

# Define a button with custom CSS style
button_style = """
    <style>
    div.stButton > button:first-child {
        background-color: #B7C9E2;
        color: #31333F;
    }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)
# Define a button
button = st.button("Click me after interacting with the plot animation!")

# If the button is clicked, display some text
if button:
    typewriter(observation)

########################################################################################################################




