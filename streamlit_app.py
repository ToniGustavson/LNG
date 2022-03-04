#%%
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

#%%
### Reading in Data
FZJcolor = pd.read_csv("Input/FZJcolor.csv")
lng_df = pd.read_excel("Input/lng_data.xlsx")
gng_df = pd.read_excel("Input/storage_data.xlsx")


### Data manipulation
lng_df["dtmi_median"] = lng_df["dtmi"].median()
lng_df["free_inventory"] = lng_df["dtmi_median"] - lng_df["lngInventory"]
xval = lng_df["gasDayStartedOn"]

gng_df["workingGasVolume_median"] = gng_df["workingGasVolume"].median()


#### Functions
def rgb_to_hex(reg_vals):
    def clamp(x): 
        return int(max(0, min(x*255, 255)))
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(reg_vals[0]), clamp(reg_vals[1]), clamp(reg_vals[2]))



### Streamlit App
st.set_page_config(
    page_title="LNG", page_icon="🚢", layout="wide" # layout="wide"
)


st.title("(In)Dependence from Russian Natural Gas")

# Plot inventory
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=lng_df["dtmi_median"], name = "Max capacity",  marker=dict(color= rgb_to_hex(FZJcolor.black))))
fig.add_trace(go.Bar(x=xval, y=lng_df["lngInventory"], name="State of charge", marker=dict(color= rgb_to_hex(FZJcolor.blue))))
# fig.add_trace(go.Scatter(x=xval, y=lng_df["lngInventory"], name="State of charge", marker=dict(color= rgb_to_hex(FZJcolor.blue)), fill='tozeroy'))
#fig.add_trace(go.Scatter(x=xval, y=lng_df["dtmi_median"], name="Free capacity", marker=dict(color= rgb_to_hex(FZJcolor.green)), fill='tonexty'))


fig.update_layout(
    title="Storage level of LNG facilities in the EU",
    yaxis_title= "LNG [10³ m³]",
    yaxis=dict(range=[0, 8000]),
    font=dict(
        size=18,
    )
)

st.plotly_chart(fig, use_container_width=True)


# Plot free capacity
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=lng_df["dtmi_median"], name = "Max capacity",  marker=dict(color= rgb_to_hex(FZJcolor.black))))
fig.add_trace(go.Bar(x=xval, y=lng_df["free_inventory"], name="Free capacity", marker=dict(color= rgb_to_hex(FZJcolor.green))))


fig.update_layout(
    title="Spare LNG storage capacity (Max capacity - State of charge)",
    yaxis_title= "LNG [10³ m³]",
    yaxis=dict(range=[0, 8000]),
    font=dict(
        size=18,
    )
)
st.plotly_chart(fig, use_container_width=True)


# Plot free capacity
fig = go.Figure()
xval_gng = lng_df["gasDayStartedOn"]
fig.add_trace(go.Line(x=xval, y=gng_df["workingGasVolume_median"], name = "Working gas Volume",  marker=dict(color= rgb_to_hex(FZJcolor.black))))

fig.add_trace(go.Bar(x=xval_gng, y=gng_df["gasInStorage"], name="State of charge", marker=dict(color= rgb_to_hex(FZJcolor.orange))))

fig.update_layout(
    title="Level of NG storages in the EU",
    yaxis_title= "NG [TWh]",
    yaxis=dict(range=[0, 1200]),
    font=dict(
        size=18,
    )
)

st.plotly_chart(fig, use_container_width=True)