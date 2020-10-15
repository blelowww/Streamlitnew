import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

# SETTING PAGE CONFIG TO WIDE MODE
st.beta_set_page_config(layout="wide")

# LOADING DATA
DATE_TIME = "date/time"
DATA_URL1 = (
    "https://raw.githubusercontent.com/Maplub/odsample/master/20190101.csv"
)
DATA_URL2 = (
    "https://raw.githubusercontent.com/Maplub/odsample/master/20190101.csv"
)
DATA_URL3 = (
    "https://raw.githubusercontent.com/Maplub/odsample/master/20190101.csv"
)
DATA_URL4 = (
    "https://raw.githubusercontent.com/Maplub/odsample/master/20190101.csv"
)
DATA_URL5 = (
    "https://raw.githubusercontent.com/Maplub/odsample/master/20190101.csv"
)

@st.cache(persist=True)
def load_data(nrows,DATA_U):
    data = pd.read_csv(DATA_U, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

data1 = load_data(100000,DATAURL1)
data2 = load_data(100000,DATAURL2)
data3 = load_data(100000,DATAURL3)
data4 = load_data(100000,DATAURL4)
data5 = load_data(100000,DATAURL5)

data = pd.concat([data1, data2,data3,data4,data5])
# CREATING FUNCTION FOR MAPS

def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lonstartl", "latstartl"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))
st.write('<h1>จรัสพงศ์ เทพรอด 6030804921</h1>',unsafe_allow_html=True)
row1_1, row1_2 = st.beta_columns((2,3))
with row1_1:
    st.title("Around the city")
    hour_selected = st.slider("Select hour to visualize", 0, 23)
    
# FILTERING DATA BY HOUR SELECTED
data = data[data[DATE_TIME].dt.hour == hour_selected]
# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
# row2_1, row2_2, row2_3, row2_4 = st.beta_columns((2,1,1,1))

zoom_level = 12
midpoint = (np.average(data["latstartl"]), np.average(data["lonstartl"]))

with row1_2:
    st.write("**All Around City from %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
    map(data, midpoint[0], midpoint[1], 11)
    
    
    
    
# histogram
# FILTERING DATA FOR THE HISTOGRAM
filtered = data[
    (data[DATE_TIME].dt.hour >= hour_selected) & (data[DATE_TIME].dt.hour < (hour_selected + 1))
    ]

hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data = pd.DataFrame({"minute": range(60), "picks": hist})

# LAYING OUT THE HISTOGRAM SECTION

st.write("")

st.write("**selected time %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("picks:Q"),
        tooltip=['minute', 'picks']
    ).configure_mark(
        opacity=0.5,
        color='red'
    ), use_container_width=True)