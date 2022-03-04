#%%
import altair as alt
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

#%%
FZJcolor = pd.read_csv("Input/FZJcolor.csv")

def rgb_to_hex(reg_vals):
    def clamp(x): 
        return int(max(0, min(x*255, 255)))
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(reg_vals[0]), clamp(reg_vals[1]), clamp(reg_vals[2]))

st.set_page_config(
    page_title="LNG", page_icon="🚢", layout="wide" # layout="wide"
)

st.title("(In)Dependence from Russian Natural Gas")

# Reading in Data
df = pd.read_excel("Input/lng_data.xlsx")

# Data manipulation
df["dtmi_median"] = df["dtmi"].median()
df["free_inventory"] = df["dtmi_median"] - df["lngInventory"]
xval = df["gasDayStartedOn"]


# st.markdown("## Pyplot - Level of LNG storage facilities in the EU")
# fig, ax = plt.subplots()
# ax.plot(xval, df["lngInventory"], label="State of charge", color = FZJcolor.blue) #range(len(df))
# ax.plot(xval, df["dtmi_median"],  label="Capacity", color = FZJcolor.orange)
# ax.legend()
# ax.set_ylim(ymin=0, ymax=8000)
# ax.set_ylabel("LNG [10$^3$ m$^3$]")
# ax.set_xlabel("Date")
# ax.grid(visible=True)
# st.pyplot(fig)


inventory = go.Bar(x=xval, y=df["lngInventory"], name="State of charge", marker=dict(color= rgb_to_hex(FZJcolor.blue)))
capacity_max = go.Line(x=xval, y=df["dtmi_median"], name = "Capacity",  marker=dict(color= rgb_to_hex(FZJcolor.orange)))

fig = go.Figure()
fig.add_trace(inventory)
fig.add_trace( capacity_max)

fig.update_layout(
    title="Storage level of LNG facilities in the EU",
    yaxis_title= "LNG [10^3 m^3]",
    yaxis=dict(range=[0, 8000]),
    font=dict(
        size=18,
    )
)
# Plot!
st.plotly_chart(fig, use_container_width=True)


### Free Capacity
free_cap = go.Bar(x=xval, y=df["free_inventory"], name="State of charge", marker=dict(color= rgb_to_hex(FZJcolor.green)))
fig = go.Figure()
fig.add_trace(free_cap)

fig.update_layout(
    title="Spare capacity (Capacity - State of charge)",
    yaxis_title= "LNG [10^3 m^3]",
    yaxis=dict(range=[0, 8000]),
    font=dict(
        size=18,
    )
)
# Plot!
st.plotly_chart(fig, use_container_width=True)