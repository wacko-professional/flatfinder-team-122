import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster
import pandas as pd
# from PIL import Image, ImageDraw, ImageFont


st.set_page_config(
    page_title="Filter")

st.markdown(
    """
    <div style='background-color: #0066cc; padding: 30px'>
        <h2 style='color: white;text-align: center;'>Research past transactions for a smarter home purchase</h2>
        <h3 style='color: #d3d3d3;text-align: center;'>Select • Filter • Visualize</h3>
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


### READ DATA ###
file_location = "updated_2017_to_now.csv"
data = pd.read_csv(file_location, index_col=0)
data = data.dropna(axis=0)
data = data.drop_duplicates().reset_index().drop("index", axis=1)

col1, mid, col2 = st.columns([2,0.5,2])

### SELECTIONS ###
with col1:
    # town
    town_filter = list(data["town"].unique())
    option_town = st.selectbox("Select a town", options=sorted(town_filter, key=str.lower))
    filtered_data = data[data["town"] == option_town]

    # distance to MRT station
    min_value_mrt = float(data["Distance_from_MRT"].min())
    max_value_mrt = float(data["Distance_from_MRT"].max())
    select_range_mrt = st.slider("Select distance to the closest MRT station (km)", min_value_mrt, max_value_mrt,
                                 (min_value_mrt, max_value_mrt), step=0.01)
    filtered_data = filtered_data[(filtered_data["Distance_from_MRT"] >= select_range_mrt[0]) & (
                filtered_data["Distance_from_MRT"] <= select_range_mrt[1])]

    # distance to mall
    min_value_mall = float(data["nearest_shopping_mall_distance"].min())
    max_value_mall = float(data["nearest_shopping_mall_distance"].max())
    select_range_mall = st.slider("Select distance to closest shopping mall (km)", min_value_mall, max_value_mall,
                                  (min_value_mall, max_value_mall), step=0.01)
    filtered_data = filtered_data[(filtered_data["nearest_shopping_mall_distance"] >= select_range_mall[0]) & (
                filtered_data["nearest_shopping_mall_distance"] <= select_range_mall[1])]

with col2:
    # flat type
    flat_filter = list(data["flat_type"].unique())
    option_flat = st.selectbox("Select a flat type", options=sorted(flat_filter, key=str.lower))
    filtered_data = filtered_data[filtered_data["flat_type"] == option_flat]


    # distance to school
    min_value_school = float(data["primary_school_distance"].min())
    max_value_school = float(data["primary_school_distance"].max())
    select_range_school = st.slider("Select distance to the closest primary school (km)", min_value_school, max_value_school, (min_value_school, max_value_school), step = 0.01)
    filtered_data = filtered_data[(filtered_data["primary_school_distance"] >= select_range_school[0]) & (filtered_data["primary_school_distance"] <= select_range_school[1])]

    # resale price slider
    min_value_price = int(data["resale_price"].min())
    max_value_price = int(data["resale_price"].max())
    select_range_price = st.slider("Select resale price (SGD$)", min_value_price, max_value_price, (min_value_price, max_value_price), step=10000)
    filtered_data = filtered_data[(filtered_data["resale_price"] >= select_range_price[0]) & (filtered_data["resale_price"] <= select_range_price[1])]


# story range
# story_filter = list(data["storey_range"].unique())
# option_story = st.multiselect("Select desired story ranges", options=sorted(story_filter, key=str.lower))
# filtered_data = filtered_data[filtered_data["storey_range"].isin(option_story)]

# floor area
# min_value_area = int(data["floor_area_sqm"].min())
# max_value_area = int(data["floor_area_sqm"].max())
# select_range_area = st.slider("Select floor area (square meter)", min_value_area, max_value_area, (min_value_area, max_value_area), step = 5)
# filtered_data = filtered_data[(filtered_data["floor_area_sqm"] >= select_range_area[0]) & (filtered_data["floor_area_sqm"] <= select_range_area[1])]

count = len(filtered_data)
if count >= 500:
    filtered_data = filtered_data.tail(500)

### MAP ###
latitude = 1.290270
longitude = 103.851959
sg_map = folium.Map(location=[latitude, longitude], zoom_start = 11, tiles = "Open Street Map", prefer_canvas=True)
mCluster = MarkerCluster().add_to(sg_map)

median_resale_price = filtered_data['resale_price'].median()

for lat, long, address, town, price, month, story, area in zip(filtered_data["Latitude"], filtered_data["Longitude"], filtered_data["address.1"], filtered_data["town"], filtered_data["resale_price"], filtered_data["month"], filtered_data["storey_range"], filtered_data["floor_area_sqm"]):
    date = month.split("-")
    month = date[1] + " 20" + date[0]
    color = "green"
    if price >= median_resale_price:
        color = "red"

    html = f"""
        <b>{address}</b>
        <p>{story} storey
            <br>{area} sqm
            <br>${price}
            <br>{month}
        </p>
    """
    popup = folium.Popup(html, max_width=170)
    folium.Marker([lat, long], popup=popup, icon=folium.Icon(color=color, icon='home')).add_to(mCluster)

st.write(str(count) + " flats found!")
if count > 500:
    st.write("(Only 500 flats with the most recent transactions are shown.)")


# create a new image with a white background
# image = Image.new(mode='RGBA', size=(500, 80), color=(255, 255, 255, 255))

# create a drawing context for the image
# draw = ImageDraw.Draw(image)

# define the font to use for the legend text
# font = ImageFont.truetype('arial.ttf', size=14)
# bold_font = ImageFont.truetype('arialbd.ttf', size=14)
# italics_font = ImageFont.truetype('ariali.ttf', size=14)

# draw the legend text and icons

# draw.text(xy=(10, 10), text='Cluster Legend', font=bold_font, fill=(0, 0, 0, 255))
# draw.text(xy=(35, 35), text='<10 flats', font=font, fill=(0, 0, 0, 255))
# draw.text(xy=(135, 35), text='<100 flats', font=font, fill=(0, 0, 0, 255))
# draw.text(xy=(235, 35), text='>=100 flats', font=font, fill=(0, 0, 0, 255))
#
# draw.ellipse(xy=(210, 30, 230, 50), fill=(255, 0, 0, 255))
# draw.ellipse(xy=(110, 30, 130, 50), fill=(255, 255, 0, 255))
# draw.ellipse(xy=(10, 30, 30, 50), fill=(0, 255, 0, 255))
#
# draw.text(xy=(10, 60), text='Click on a cluster to view in more detail', font=italics_font, fill=(0, 0, 0, 255))

# save the image as a PNG file
# image.save('cluster_legend.png', format='PNG')
st.image('cluster_legend.png')


# create a new image with a white background
# image = Image.new(mode='RGBA', size=(500, 80), color=(255, 255, 255, 255))

# create a drawing context for the image
# draw = ImageDraw.Draw(image)

# draw the legend text and icons

# draw.text(xy=(10, 10), text='Marker Legend', font=bold_font, fill=(0, 0, 0, 255))
# draw.text(xy=(30, 35), text='Below median resale price', font=font, fill=(0, 0, 0, 255))
# draw.text(xy=(230, 35), text='Above median resale price', font=font, fill=(0, 0, 0, 255))
# draw.rectangle(xy=(10, 35, 25, 50), fill=(0, 255, 0, 255))
# draw.rectangle(xy=(210, 35, 225, 50), fill=(255, 0, 0, 255))

# save the image as a PNG file
# image.save('legend.png', format='PNG')
st.image('legend.png')

#sw = filtered_data[["Latitude", "Longitude"]].min().values.tolist()
#ne = filtered_data[["Latitude", "Longitude"]].max().values.tolist()

#sg_map.fit_bounds([sw, ne], padding_top_left = (0, 0), padding_bottom_right=(10,10))

st_data = st_folium(sg_map, width=700)



