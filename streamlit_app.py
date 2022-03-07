#%%
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from preprocessing import *




# Get Data
FZJcolor = get_fzjColor()
lng_df = get_lng_storage()
gng_df = get_ng_storage()
opal_df = get_OPAL()
nel_df = get_NEL()
ng_share = get_ng_share()
solid_fuel_share = get_solid_fuel_share()
crude_oil_share = get_crude_oil_share()

xval = lng_df["gasDayStartedOn"]

### Functions 

def annual_mean(df, scalefac):
    annual_mean_val = df.mean()*365/scalefac
    annual_mean_val = int(round(annual_mean_val, 0))
    return annual_mean_val

def get_color(key, default_col="blue"):
    return {"Russia": FZJcolor.get(default_col)}.get(key, FZJcolor.get("grey1") )



font_size = 18

### Streamlit App
st.set_page_config(
    page_title="Energy Independence", page_icon="🇪🇺", layout="wide" # layout="wide" 🚢
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown("# Energy imports from Russia and possible alternatives")

st.markdown("## EU energy imports by country of origin")

cols = st.columns(3)
# Natrural Gas Import
cols[0].markdown("### Natural gas")
# cols[0].markdown("[10$^3$ TWh/a]")
colors = [get_color(x, default_col="blue4") for x in ng_share.index]
fig = go.Figure()
fig.add_trace(go.Pie(labels=ng_share.index, values = ng_share.value, hole=.3, marker=dict(colors=colors)))
cols[0].plotly_chart(fig, use_container_width=True)
cols[0].caption("Source: Eurostat, 2020")

# Solid Fuels
cols[1].markdown("### Solid fuels")
colors = [get_color(x, default_col="black") for x in solid_fuel_share.index]
fig = go.Figure()
fig.add_trace(go.Pie(labels=solid_fuel_share.index, values = solid_fuel_share.value, hole=.3, marker=dict(colors=colors)))

cols[1].plotly_chart(fig, use_container_width=True)
cols[1].caption("Source: Eurostat, 2019")

# Crude oil imports
cols[2].markdown("### Crude oil")
colors = [get_color(x, default_col="black3") for x in crude_oil_share.index]
fig = go.Figure()
fig.add_trace(go.Pie(labels=crude_oil_share.index, values = crude_oil_share.value, hole=.3, marker=dict(colors=colors)))

cols[2].plotly_chart(fig, use_container_width=True)
cols[2].caption("Source: Eurostat, 2019")


st.markdown("## Pipeline import of natural gas")

fig = go.Figure()
fig.add_trace(go.Scatter(x=xval, y=opal_df["value"],stackgroup='one', name = f"OPAL (Nord Stream 1, Ø {annual_mean(opal_df['value'], 10**3)} TWh/a)",  marker=dict(color= FZJcolor.get("blue2"))))
fig.add_trace(go.Scatter(x=xval, y=nel_df["value"],stackgroup='one', name=f"NEL (Nord Stream 1, Ø {int(nel_df['value'].mean()*365/10**3)} TWh/a)", marker=dict(color=FZJcolor.get("blue3")))) #, fill = 'tozeroy'


fig.update_layout(
    title="EU pipeline imports from Russia",
    yaxis_title= "NG [GWh/d]",
    yaxis=dict(range=[0, 2700]),
    font=dict(
        size=font_size,
    ),
    barmode='stack',
)


st.plotly_chart(fig, use_container_width=True)
st.caption("Source: ENTSOG, 2022")


st.markdown("## Storages")

col1, col2 = st.columns(2)
col1.markdown("### Liquefied Natural Gas (LNG)")
col2.markdown("### Natural Gas (NG)")

############
###  LNG
############


# Plot inventory LNG
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=lng_df["dtmi_median"], name = "Max capacity",  marker=dict(color= FZJcolor.get("black"))))
fig.add_trace(go.Scatter(x=xval, y=lng_df["lngInventory"], name="State of charge", marker=dict(color=FZJcolor.get("blue")), fill = 'tozeroy'))


fig.update_layout(
    title="Storage level of LNG facilities in the EU",
    yaxis_title= "LNG [TWh]",
    yaxis=dict(range=[0, 60]),
    font=dict(
        size=font_size,
    )
)
col1.plotly_chart(fig, use_container_width=True)
col1.caption("Source: GIE, 2022")

# Plot free capacity LNG
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=lng_df["dtmi_median"], name = "Max capacity",  marker=dict(color= FZJcolor.get("black"))))
fig.add_trace(go.Scatter(x=xval, y=lng_df["free_inventory"], name="Free capacity", marker=dict(color=FZJcolor.get("green")), fill = 'tozeroy'))


fig.update_layout(
    title="Spare LNG storage capacity (Max capacity - State of charge)",
    yaxis_title= "LNG [TWh]",
    yaxis=dict(range=[0, 60]),
    font=dict(
        size=font_size,
    )
)
col1.plotly_chart(fig, use_container_width=True)
col1.caption("Source: GIE, 2022")


# Send Out
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=lng_df["dtrs_median"], name = f"Max send out (Ø {int(lng_df['dtrs_median'].mean()*365/10**3)} TWh/a)",  marker=dict(color= FZJcolor.get("black"))))
fig.add_trace(go.Scatter(x=xval, y=lng_df["sendOut"], name=f"Send out rate (Ø {int(lng_df['sendOut'].mean()*365/10**3)} TWh/a)", marker=dict(color= FZJcolor.get("orange"))))


fig.update_layout(
    title="Send out of LNG",
    yaxis_title= "LNG [GWh/d]",
    yaxis=dict(range=[0, 7000]),
    font=dict(
        size=font_size,
    )
)
col1.plotly_chart(fig, use_container_width=True)
col1.caption("Source: GIE, 2022")

############
###  NG
############

# Plot NG
fig = go.Figure()
xval_gng = lng_df["gasDayStartedOn"]
fig.add_trace(go.Line(x=xval, y=gng_df["workingGasVolume_median"], name = "Max capacity",  marker=dict(color= FZJcolor.get("black"))))
fig.add_trace(go.Scatter(x=xval_gng, y=gng_df["gasInStorage"], name="State of charge", marker=dict(color= FZJcolor.get("blue")), fill = 'tozeroy'))

fig.update_layout(
    title="Storage level NG in the EU",
    yaxis_title= "NG [TWh]",
    yaxis=dict(range=[0, 1200]),
    font=dict(
        size=font_size,
    )
)

col2.plotly_chart(fig, use_container_width=True)
col2.caption("Source: GIE, 2022")

# Plot NG free
fig = go.Figure()
xval_gng = lng_df["gasDayStartedOn"]
fig.add_trace(go.Line(x=xval, y=gng_df["workingGasVolume_median"], name = "Max capacity",  marker=dict(color= FZJcolor.get("black"))))
# fig.add_trace(go.Bar(x=xval_gng, y=gng_df["gasInStorage"], name="State of charge", marker=dict(color= rgb_to_hex(FZJcolor.orange))))
fig.add_trace(go.Scatter(x=xval_gng, y=gng_df["free_cap"], name="Free capacity", marker=dict(color= FZJcolor.get("green")), fill = 'tozeroy'))

fig.update_layout(
    title="Spare NG storage capacity (Max capacity - State of charge)",
    yaxis_title= "NG [TWh]",
    yaxis=dict(range=[0, 1200]),
    font=dict(
        size=font_size,
    )
)
col2.plotly_chart(fig, use_container_width=True)
col2.caption("Source: GIE, 2022")

# Withdrawal
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=gng_df["withdrawalCapacity_median"], name = f"Max withdrawl (Ø {int(gng_df['withdrawalCapacity_median'].mean()*365/10**3)} TWh/a)",  marker=dict(color= FZJcolor.get("black"))))
fig.add_trace(go.Scatter(x=xval, y=gng_df["withdrawal"], name=f"Withdrawl rate (Ø {int(gng_df['withdrawal'].mean()*365/10**3)} TWh/a)", marker=dict(color= FZJcolor.get("orange"))))


fig.update_layout(
    title="Withdrawal of NG",
    yaxis_title= "NG [GWh/d]",
    yaxis=dict(range=[0, 20000]),
    font=dict(
        size=font_size,
    )
)
col2.plotly_chart(fig, use_container_width=True)
col2.caption("Source: GIE, 2022")